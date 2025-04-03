from datetime import datetime, timedelta, timezone
from enum import IntEnum as _IntEnum
from typing import Any, Optional, Type, TypeVar, cast

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.operators import OperatorType


class UTCDateTime(types.TypeDecorator[datetime]):
    """Store aware datetimes and return them in UTC."""

    impl = types.DateTime
    cache_ok = True

    def __init__(self) -> None:
        super().__init__(timezone=True)

    def __repr__(self) -> str:
        return "UTCDateTime()"

    def coerce_compared_value(
        self, op: OperatorType | None, value: Any
    ) -> types.TypeEngine[Any]:
        if isinstance(value, timedelta):
            return types.Interval()
        return self

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.utcoffset() is None:
            raise ValueError(
                "Datetime values must have timezone information. "
                "Use datetime.now(timezone.utc), or annotate the field with "
                "NaiveDatetime for naive storage."
            )
        return value.astimezone(timezone.utc)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.utcoffset() is None:
            # Databases without timezone support store UTC without an offset.
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)


_TIntEnum = TypeVar("_TIntEnum", bound="_IntEnum")


class IntEnum(types.TypeDecorator):  # type: ignore
    """TypeDecorator for Integer-enum conversion.

    Automatically converts Python enum.IntEnum <-> database integers.

    Args:
        enum_type (enum.IntEnum): Integer enum class (subclass of enum.IntEnum)

    Example:
        >>> class HeroStatus(enum.IntEnum):
        ...     ACTIVE = 1
        ...     DISABLE = 2
        >>>>
        >>> from sqlmodel import IntEnum
        >>> class Hero(SQLModel):
        ...     hero_status: HeroStatus = Field(sa_type=sqlmodel.IntEnum(HeroStatus))
        >>> user.hero_status == Status.ACTIVE      # Loads back as enum

    Returns:
        Optional[enum.IntEnum]: Converted enum instance (None if database value is NULL)

    Raises:
        TypeError: For invalid enum types
    """

    impl = types.Integer

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
