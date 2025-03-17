from typing import Any, List, Type, TypeVar, cast, get_args

from pydantic import BaseModel
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSONB  # for Postgres JSONB
from sqlalchemy.engine.interfaces import Dialect

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


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

    def __init__(
        self,
        model_class: Type[BaseModelType] | Type[list[BaseModelType]],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.model_class = model_class  # Pydantic model class to use

    def process_bind_param(self, value: Any, dialect) -> dict | list[dict] | None:  # noqa: ANN401, ARG002, ANN001
        if value is None:
            return None
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        if isinstance(value, list):
            return [
                m.model_dump(mode="json") if isinstance(m, BaseModel) else m
                for m in value
            ]
        return value

    def process_result_value(
        self, value: Any, dialect
    ) -> BaseModelType | List[BaseModelType] | None:  # noqa: ANN401, ARG002, ANN001
        # Called when loading from DB: convert dict to Pydantic model instance
        if value is None:
            return None
        if isinstance(value, dict):
            return self.model_class.model_validate(value)  # type: ignore
        if isinstance(value, list):
            return [get_args(self.model_class)[0].model_validate(v) for v in value]  # type: ignore
        return value
