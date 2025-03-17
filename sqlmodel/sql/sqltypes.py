from typing import Any, cast

from pydantic import BaseModel
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSONB  # for Postgres JSONB
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


class PydanticJSONB(types.TypeDecorator):  # type: ignore
    """Custom type to automatically handle Pydantic model serialization."""

    impl = JSONB  # use JSONB type in Postgres (fallback to JSON for others)
    cache_ok = True  # allow SQLAlchemy to cache results

    def __init__(self, model_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class  # Pydantic model class to use

    def process_bind_param(self, value, dialect):
        # Called when storing to DB: convert Pydantic model to a dict (JSON-serializable)
        if value is None:
            return None
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value  # assume it's already a dict

    def process_result_value(self, value, dialect):
        # Called when loading from DB: convert dict to Pydantic model instance
        if value is None:
            return None
        return self.model_class.parse_obj(value)  # instantiate Pydantic model
