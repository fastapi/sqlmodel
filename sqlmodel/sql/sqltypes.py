from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from pydantic import BaseModel
from pydantic_core import to_jsonable_python
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
                m.model_dump(mode="json")
                if isinstance(m, BaseModel)
                else to_jsonable_python(m)
                for m in value
            ]
        if isinstance(value, dict):
            return {
                k: v.model_dump(mode="json")
                if isinstance(v, BaseModel)
                else to_jsonable_python(v)
                for k, v in value.items()
            }

        return to_jsonable_python(value)

    def process_result_value(
        self, value: Any, dialect: Any
    ) -> Optional[Union[BaseModelType, List[BaseModelType], Dict[str, BaseModelType]]]:  # noqa: ANN401, ARG002, ANN001
        if value is None:
            return None
        if isinstance(value, dict):
            # If model_class is a Dict type hint, handle key-value pairs
            origin = get_origin(self.model_class)
            if origin is dict:
                model_class = get_args(self.model_class)[
                    1
                ]  # Get the value type (the model)
                return {k: model_class.model_validate(v) for k, v in value.items()}
            # Regular case: the whole dict represents a single model
            return self.model_class.model_validate(value)  # type: ignore
        if isinstance(value, list):
            # If model_class is a List type hint
            origin = get_origin(self.model_class)
            if origin is list:
                model_class = get_args(self.model_class)[0]
                return [model_class.model_validate(v) for v in value]
            # Fallback case (though this shouldn't happen given our __init__ types)
            return [self.model_class.model_validate(v) for v in value]  # type: ignore

        raise TypeError(
            f"Unsupported type for PydanticJSONB from database: {type(value)}. Expected a dictionary or list."
        )
