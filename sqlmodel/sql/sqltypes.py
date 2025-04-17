from enum import IntEnum as _IntEnum
from typing import Any, Optional, Type, TypeVar, cast

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect

_TIntEnum = TypeVar("_TIntEnum", bound="_IntEnum")


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)


class IntEnum(types.TypeDecorator):  # type: ignore
    impl = types.Integer
    cache_ok = True

    def __init__(self, enum_type: Type[_TIntEnum], *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        # validate the input enum type
        if not issubclass(enum_type, _IntEnum):
            raise TypeError("Input must be enum.IntEnum")

        self.enum_type = enum_type

    def process_result_value(  # type: ignore[override]
        self,
        value: Optional[int],
        dialect: Dialect,
    ) -> Optional[_TIntEnum]:
        if value is None:
            return None

        result = self.enum_type(value)
        return result

    def process_bind_param(
        self,
        value: Optional[_TIntEnum],
        dialect: Dialect,
    ) -> Optional[int]:
        if value is None:
            return None

        result = value.value
        return result
