"""
Deferred Column Property implementation for SQLModel.

This module provides deferred_column_property function that creates column properties
with safe deferred loading - returning fallback values instead of raising DetachedInstanceError.
"""

from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import ColumnProperty, column_property
from sqlalchemy.orm.attributes import set_committed_value


def deferred_column_property(
    expression: Any, *, fallback_value: Any, deferred: bool = True, **kwargs: Any
) -> ColumnProperty:
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
        A standard ColumnProperty instance with event listeners for fallback handling

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

    # Create a standard ColumnProperty
    prop = column_property(expression, **kwargs)

    # Store fallback_value as attribute for later use in event setup
    prop._deferred_fallback_value = fallback_value

    # Hook into instrument_class to set up event listeners
    original_instrument_class = prop.instrument_class

    def instrument_class_with_events(mapper):
        """Enhanced instrument_class that sets up fallback event listeners"""
        result = original_instrument_class(mapper)

        # Set up event listeners for automatic fallback values
        _setup_fallback_listeners(mapper, prop.key, fallback_value)

        return result

    prop.instrument_class = instrument_class_with_events

    return prop


def _setup_fallback_listeners(mapper, key: str, fallback_value: Any):
    """Set up event listeners to automatically set fallback values on load/refresh"""
    class_type = mapper.class_

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
