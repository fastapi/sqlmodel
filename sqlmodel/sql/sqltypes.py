import uuid
from typing import Any, Optional, cast

from sqlalchemy import CHAR, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.type_api import TypeEngine


class AutoString(types.TypeDecorator):  # type: ignore

    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))  # type: ignore
        return super().load_dialect_impl(dialect)


# Reference form SQLAlchemy docs: https://docs.sqlalchemy.org/en/14/core/custom_types.html#backend-agnostic-guid-type
# with small modifications
class GUID(types.TypeDecorator):  # type: ignore
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine:  # type: ignore
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())  # type: ignore
        else:
            return dialect.type_descriptor(CHAR(32))  # type: ignore

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                # hexstring
                return value.hex

    def process_result_value(self, value: Any, dialect: Dialect) -> Optional[uuid.UUID]:
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return cast(uuid.UUID, value)
