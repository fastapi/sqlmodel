from enum import Enum
from typing import Any, Optional, Sequence, Tuple, Type, Union, cast

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)


class UnionEnum(types.TypeDecorator):  # type: ignore
    """
    A TypeDecorator that handles Union of Enum types.

    This type stores enum values as strings in the database but converts them
    back to the appropriate Enum member when reading. It supports multiple
    Enum types in a Union.

    Example:
        class StatusA(str, Enum):
            active = "active"

        class StatusB(str, Enum):
            inactive = "inactive"

        # Field annotation: Union[StatusA, StatusB]
        # Stored in DB as VARCHAR, returned as Enum instance
    """

    impl = types.String
    cache_ok = True

    def __init__(
        self,
        *enum_types: Type[Enum],
        length: Optional[int] = None,
    ):
        self.enum_types: Tuple[Type[Enum], ...] = enum_types
        # Build lookup dict: value -> enum member
        self._value_to_enum: dict[str, Enum] = {}
        max_len = 0
        for enum_type in enum_types:
            for member in enum_type:
                value = member.value if hasattr(member, "value") else str(member)
                str_value = str(value)
                self._value_to_enum[str_value] = member
                max_len = max(max_len, len(str_value))

        # Set the impl with appropriate length
        if length is not None:
            self.impl = types.String(length)
        elif max_len > 0:
            # Add some buffer for future enum values
            self.impl = types.String(max(max_len + 10, 50))
        super().__init__()

    def process_bind_param(
        self, value: Optional[Union[Enum, str]], dialect: Dialect
    ) -> Optional[str]:
        """Convert Enum to string value when inserting into database."""
        if value is None:
            return None
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[Enum]:
        """Convert string value back to Enum when reading from database."""
        if value is None:
            return None
        enum_member = self._value_to_enum.get(value)
        if enum_member is not None:
            return enum_member
        # If not found in lookup, return the raw value
        # This handles cases where the DB contains values not in current enums
        return value  # type: ignore

    def copy(self, **kwargs: Any) -> "UnionEnum":
        """Create a copy of this type."""
        return UnionEnum(*self.enum_types)
