"""
Deferred Column Property implementation for SQLModel.

This module provides deferred_column_property function that creates column properties
with safe deferred loading - returning fallback values instead of raising DetachedInstanceError.
"""

from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.attributes import set_committed_value
from sqlalchemy.orm.strategies import DeferredColumnLoader, _state_session


class SafeDeferredColumnLoader(DeferredColumnLoader):
    """
    A simplified deferred column loader that works with event-based fallback setting.
    The main fallback logic is now handled by event listeners in SafeColumnProperty.
    """

    def __init__(self, parent, strategy_key, fallback_value=None):
        super().__init__(parent, strategy_key)
        self.fallback_value = fallback_value

    def _load_for_state(self, state, passive):
        """
        Override to handle session-related errors gracefully.
        Fallback values are pre-set by event listeners, so we mainly handle exceptions here.
        """
        from sqlalchemy.orm import LoaderCallableStatus

        if not state.key:
            return LoaderCallableStatus.ATTR_EMPTY

        # Check passive flags
        from sqlalchemy.orm import PassiveFlag

        if not passive & PassiveFlag.SQL_OK:
            return LoaderCallableStatus.PASSIVE_NO_RESULT

        # Check if we have a session before attempting to load
        session = _state_session(state)
        if session is None:
            # No session - return the fallback that should be already set by event listener
            # If for some reason it's not set, the fallback value will be used
            return LoaderCallableStatus.PASSIVE_NO_RESULT

        # Try normal loading with error handling for async issues
        try:
            return super()._load_for_state(state, passive)
        except Exception as e:
            # Handle async-related errors (MissingGreenlet, etc.)
            error_msg = str(e).lower()
            if any(
                keyword in error_msg
                for keyword in [
                    "greenlet",
                    "await_only",
                    "asyncio",
                    "async",
                    "missinggreenlet",
                ]
            ):
                # This is an async-related error
                # The fallback value should already be set by event listener
                return LoaderCallableStatus.PASSIVE_NO_RESULT
            # For other exceptions, re-raise them
            raise


class SafeColumnProperty(ColumnProperty):
    """
    Custom ColumnProperty that automatically sets fallback values on load events.
    This ensures deferred properties always have a safe fallback value available.
    """

    def __init__(self, *args, fallback_value=None, **kwargs):
        self.fallback_value = fallback_value
        super().__init__(*args, **kwargs)

    def instrument_class(self, mapper):
        """Override to set up event listeners for automatic fallback value setting"""
        result = super().instrument_class(mapper)

        # Set up event listeners to automatically set fallback values
        self._setup_fallback_listeners(mapper)

        return result

    def _setup_fallback_listeners(self, mapper):
        """Set up event listeners to automatically set fallback values on load/refresh"""
        class_type = mapper.class_
        key = self.key
        fallback_value = self.fallback_value

        @event.listens_for(class_type, "load")
        def _set_deferred_fallback_on_load(target, context):
            """Set fallback value when object is loaded from database"""
            if key not in target.__dict__:
                set_committed_value(target, key, fallback_value)

        @event.listens_for(class_type, "refresh")
        def _set_deferred_fallback_on_refresh(target, context, attrs):
            """Set fallback value when object is refreshed"""
            if key not in target.__dict__ or attrs is None or key in attrs:
                set_committed_value(target, key, fallback_value)

    def do_init(self):
        """Override to set our custom strategy after parent initialization."""
        super().do_init()

        # Replace the strategy with our safe version if it's deferred
        if self.deferred and hasattr(self, "strategy"):
            # Create our safe loader with the same parameters as the original
            original_strategy = self.strategy

            # Create new strategy with proper initialization
            safe_strategy = SafeDeferredColumnLoader(
                parent=self,  # The ColumnProperty itself
                strategy_key=original_strategy.strategy_key,
                fallback_value=self.fallback_value,
            )

            self.strategy = safe_strategy


def deferred_column_property(
    expression: Any, *, fallback_value: Any, deferred: bool = True, **kwargs: Any
) -> SafeColumnProperty:
    """
    Create a deferred column property that returns a fallback value instead of raising
    DetachedInstanceError when accessed on a detached instance.

    This function behaves exactly like SQLAlchemy's column_property, but with safe
    deferred loading behavior when the session is detached.

    Args:
        expression: The SQL expression for the column property
        fallback_value: Value to return when property cannot be loaded (required)
        deferred: Whether to defer loading the property (defaults to True)
        **kwargs: Additional arguments passed to column_property

    Returns:
        A SafeColumnProperty instance

    Example:
        ```python
        class User(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            user_id: Optional[int] = None

            @classmethod
            def __declare_last__(cls):
                cls.computed_value = deferred_column_property(
                    cls.__table__.c.user_id * 2,
                    fallback_value=0,
                    deferred=True
                )
        ```
    """
    kwargs["deferred"] = deferred
    return SafeColumnProperty(expression, fallback_value=fallback_value, **kwargs)
