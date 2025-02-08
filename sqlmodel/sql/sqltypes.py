from typing import Any, cast

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect


class AutoString(types.TypeDecorator):  # type: ignore
    """
    Determines the best sqlalchemy string type based on the database dialect.

    For example, when using Postgres this will return sqlalchemy's String()
    """

    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)
