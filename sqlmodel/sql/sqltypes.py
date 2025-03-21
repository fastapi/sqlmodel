from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast, get_args

from pydantic import BaseModel
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSONB  # for Postgres JSONB
from sqlalchemy.engine.interfaces import Dialect

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> types.TypeEngine[Any]:
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
        model_class: Union[
            Type[BaseModelType],
            Type[List[BaseModelType]],
            Type[Dict[str, BaseModelType]],
        ],
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.model_class = model_class  # Pydantic model class to use

    def process_bind_param(
        self, value: Any, dialect: Any
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:  # noqa: ANN401, ARG002, ANN001
        if value is None:
            return None
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        if isinstance(value, list):
            return [
                m.model_dump(mode="json") if isinstance(m, BaseModel) else m
                for m in value
            ]
        if isinstance(value, dict):
            return {
                k: v.model_dump(mode="json") if isinstance(v, BaseModel) else v
                for k, v in value.items()
            }
        return value

    def process_result_value(
        self, value: Any, dialect: Any
    ) -> Optional[Union[BaseModelType, List[BaseModelType], Dict[str, BaseModelType]]]:  # noqa: ANN401, ARG002, ANN001
        if value is None:
            return None
        if isinstance(value, dict):
            # If model_class is a Dict type hint, handle key-value pairs
            if (
                hasattr(self.model_class, "__origin__")
                and self.model_class.__origin__ is dict
            ):
                model_class = get_args(self.model_class)[
                    1
                ]  # Get the value type (the model)
                return {k: model_class.model_validate(v) for k, v in value.items()}
            # Regular case: the whole dict represents a single model
            return self.model_class.model_validate(value)  # type: ignore
        if isinstance(value, list):
            # If model_class is a List type hint
            if (
                hasattr(self.model_class, "__origin__")
                and self.model_class.__origin__ is list
            ):
                model_class = get_args(self.model_class)[0]
                return [model_class.model_validate(v) for v in value]
            # Fallback case (though this shouldn't happen given our __init__ types)
            return [self.model_class.model_validate(v) for v in value]  # type: ignore
        return value
