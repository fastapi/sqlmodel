from datetime import datetime, timezone
from typing import Any, cast

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect


class UTCDateTime(types.TypeDecorator[datetime]):
    """Store aware datetimes and return them in UTC."""

    impl = types.DateTime
    cache_ok = True

    def __init__(self) -> None:
        super().__init__(timezone=True)

    def __repr__(self) -> str:
        return "UTCDateTime()"

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


class AutoString(types.TypeDecorator):
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)
