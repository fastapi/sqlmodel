"""
Deferred Column Property implementation for SQLModel.

This module provides deferred_column_property function that creates column properties
with safe deferred loading - returning fallback values instead of raising DetachedInstanceError.
"""

from typing import Any

from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.strategies import DeferredColumnLoader, _state_session


class SafeAttributeWrapper:
    """
    A simple wrapper around InstrumentedAttribute that checks session validity
    on every access and returns fallback values when needed.
    """

    def __init__(self, original_attr, fallback_value):
        self.original_attr = original_attr
        self.fallback_value = fallback_value
        # Copy important attributes from original
        self.__name__ = getattr(original_attr, "__name__", None)
        self.__doc__ = getattr(original_attr, "__doc__", None)

    def __get__(self, instance, owner):
        """Intercept attribute access to check session validity"""
        if instance is None:
            return self

        # Check session state before accessing
        try:
            state = instance._sa_instance_state
            session = _state_session(state)

            # First check for invalid async context - regardless of session state
            if self._is_invalid_async_context(state):
                return self.fallback_value

            # If no session, check if attribute is already loaded
            if session is None:
                if (
                    hasattr(instance, "__dict__")
                    and self.original_attr.key in instance.__dict__
                ):
                    # Attribute was loaded previously but session is now invalid
                    # However, if we detect we SHOULD be in async context but aren't,
                    # return fallback instead of cached value
                    return instance.__dict__[self.original_attr.key]
                else:
                    # Not loaded and no session - return fallback
                    return self.fallback_value

            # Session is valid, proceed with normal access through original attribute
            return self.original_attr.__get__(instance, owner)

        except Exception as e:
            # If any error occurs during access, check if it's async-related
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
                return self.fallback_value
            # For other errors, re-raise
            raise

    def __set__(self, instance, value):
        """Delegate setting to original attribute"""
        return self.original_attr.__set__(instance, value)

    def __delete__(self, instance):
        """Delegate deletion to original attribute"""
        return self.original_attr.__delete__(instance)

    def _is_invalid_async_context(self, state):
        """Check if we're in an invalid async context that would cause MissingGreenlet"""
        try:
            # Check if we have async session
            if hasattr(state, "async_session") and state.async_session is not None:
                # We have async session, need to check greenlet context
                try:
                    import greenlet

                    current = greenlet.getcurrent()
                    # If we're not in a greenlet context but have async session,
                    # accessing deferred attributes will fail
                    if current is None or current.parent is None:
                        return True
                except ImportError:
                    # No greenlet support, assume we're in invalid context if async_session exists
                    return True
            return False
        except Exception:
            # If any check fails, assume we're in invalid context
            return True

    # Make wrapper transparent to SQLAlchemy inspection system
    def __getattr__(self, name):
        """Proxy all other attributes to the original InstrumentedAttribute"""
        return getattr(self.original_attr, name)

    def _sa_inspect_type(self):
        """Support SQLAlchemy inspection by delegating to original attribute"""
        if hasattr(self.original_attr, "_sa_inspect_type"):
            return self.original_attr._sa_inspect_type()
        return None


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
        DetachedInstanceError or MissingGreenlet when session is None or async context is missing.
        """
        from sqlalchemy.orm import LoaderCallableStatus
        from sqlalchemy.orm.attributes import set_committed_value

        if not state.key:
            return LoaderCallableStatus.ATTR_EMPTY

        # Check passive flags
        from sqlalchemy.orm import PassiveFlag

        if not passive & PassiveFlag.SQL_OK:
            return LoaderCallableStatus.PASSIVE_NO_RESULT

        # Check if the attribute is already loaded
        if self.key not in state.unloaded:
            # Attribute is already loaded, use parent implementation
            return super()._load_for_state(state, passive)

        # Check if we have a session before attempting to load
        session = _state_session(state)
        if session is None:
            # No session available, set fallback value directly on the instance
            instance = state.obj()
            if instance is not None:
                set_committed_value(instance, self.key, self.fallback_value)
                return LoaderCallableStatus.ATTR_WAS_SET
            return self.fallback_value

        # Check if this is an AsyncSession that might cause MissingGreenlet
        async_session = state.async_session
        if async_session is not None:
            # We have an async session, check if we're in proper async context
            try:
                # Try to import greenlet to check context
                import greenlet

                current_greenlet = greenlet.getcurrent()
                # If we're in the main thread without proper async context,
                # the greenlet will not have a proper parent or spawn context
                if current_greenlet.parent is None and not hasattr(
                    current_greenlet, "_spawning_greenlet"
                ):
                    # We're likely in sync code trying to access async session attributes
                    instance = state.obj()
                    if instance is not None:
                        set_committed_value(instance, self.key, self.fallback_value)
                        return LoaderCallableStatus.ATTR_WAS_SET
                    return self.fallback_value
            except (ImportError, AttributeError):
                # greenlet not available, but we know it's an async session
                # in sync context - return fallback
                instance = state.obj()
                if instance is not None:
                    set_committed_value(instance, self.key, self.fallback_value)
                    return LoaderCallableStatus.ATTR_WAS_SET
                return self.fallback_value

        # Final attempt with error handling for any remaining async issues
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
                # This is an async-related error, set fallback value
                instance = state.obj()
                if instance is not None:
                    set_committed_value(instance, self.key, self.fallback_value)
                    return LoaderCallableStatus.ATTR_WAS_SET
                return self.fallback_value
            # For other exceptions, re-raise them
            raise
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
                # This is an async-related error, set fallback value directly
                instance = state.obj()
                if instance is not None:
                    set_committed_value(instance, self.key, self.fallback_value)
                    return LoaderCallableStatus.ATTR_WAS_SET
                return self.fallback_value
            # For other exceptions, re-raise them
            raise


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
