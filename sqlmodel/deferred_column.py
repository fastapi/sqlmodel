"""
Deferred Column Property implementation for SQLModel.

This module provides deferred_column_property function that creates column properties
with safe deferred loading - returning fallback values instead of raising DetachedInstanceError.
"""

from typing import Any

from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.strategies import DeferredColumnLoader, _state_session


class SafeDeferredColumnLoader(DeferredColumnLoader):
    """
    A custom deferred column loader that returns a fallback value instead of
    raising DetachedInstanceError when the session is detached.
    """

    def __init__(self, parent, strategy_key, fallback_value=None):
        super().__init__(parent, strategy_key)
        self.fallback_value = fallback_value

    def _load_for_state(self, state, passive):
        """
        Override the default behavior to return fallback value instead of raising
        DetachedInstanceError when session is None.
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
            # No session available, return fallback value directly
            return self.fallback_value

        # We have a session, use the parent implementation
        return super()._load_for_state(state, passive)


class SafeColumnProperty(ColumnProperty):
    """
    Custom ColumnProperty that uses SafeDeferredColumnLoader for deferred loading.
    """

    def __init__(self, *args, fallback_value=None, **kwargs):
        self.fallback_value = fallback_value
        super().__init__(*args, **kwargs)

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
