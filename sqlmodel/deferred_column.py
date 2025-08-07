"""
Deferred Column Property implementation for SQLModel.

This module provides deferred_column_property function that creates column properties
with safe deferred loading - returning fallback values instead of raising DetachedInstanceError.
"""

from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

from sqlalchemy import event
from sqlalchemy.orm import column_property
from sqlalchemy.orm.attributes import set_committed_value

if TYPE_CHECKING:
    from sqlalchemy.orm._typing import _ORMColumnExprArgument
    from sqlalchemy.orm.interfaces import PropComparator
    from sqlalchemy.orm.properties import MappedSQLExpression
    from sqlalchemy.sql._typing import _InfoType

_T = TypeVar("_T")


def deferred_column_property(
    expression: "_ORMColumnExprArgument[_T]",
    *additional_expressions: "_ORMColumnExprArgument[Any]",
    fallback_value: Any,
    group: Optional[str] = None,
    deferred: bool = True,
    raiseload: bool = False,
    comparator_factory: Optional[Type["PropComparator[_T]"]] = None,
    active_history: bool = False,
    expire_on_flush: bool = True,
    info: Optional["_InfoType"] = None,
    doc: Optional[str] = None,
) -> "MappedSQLExpression[_T]":
    """
    Create a deferred column property that returns a fallback value instead of raising
    DetachedInstanceError when accessed on a detached instance.

    This function behaves exactly like SQLAlchemy's column_property, but with safe
    deferred loading behavior when the session is detached.

    Args:
        expression: The SQL expression for the column property
        *additional_expressions: Additional SQL expressions for the column property
        fallback_value: Value to return when property cannot be loaded (required)
        group: A group name for this property when marked as deferred
        deferred: Whether to defer loading the property (defaults to True)
        raiseload: When True, loading this property will raise an error
        comparator_factory: A class which extends PropComparator for custom SQL clause generation
        active_history: When True, indicates that the "previous" value should be loaded when replaced
        expire_on_flush: Whether this property expires on session flush
        info: Optional data dictionary which will be populated into the MapperProperty.info attribute
        doc: Optional string that will be applied as the doc on the class-bound descriptor

    Returns:
        A MappedSQLExpression instance with event listeners for fallback handling

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

    # Create a standard ColumnProperty with all the parameters
    prop = column_property(
        expression,
        *additional_expressions,
        group=group,
        deferred=deferred,
        raiseload=raiseload,
        comparator_factory=comparator_factory,
        active_history=active_history,
        expire_on_flush=expire_on_flush,
        info=info,
        doc=doc,
    )

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
        # Only set fallback if key is not in __dict__ (not loaded)
        if key not in target.__dict__:
            set_committed_value(target, key, fallback_value)

    @event.listens_for(class_type, "refresh")
    def _set_deferred_fallback_on_refresh(target, context, attrs):
        """Set fallback value when object is refreshed"""
        if key not in target.__dict__ or attrs is None or key in attrs:
            set_committed_value(target, key, fallback_value)
