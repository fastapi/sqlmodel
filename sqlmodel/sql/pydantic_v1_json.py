"""Кастомный тип для сериализации/десериализации JSON"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, parse_obj_as
from sqlalchemy import types
from sqlalchemy.engine import Dialect


class PydanticJSONv1(types.TypeDecorator):  # type: ignore
    """Type to store Pydantic models as JSON data at database"""

    impl = types.JSON
    cache_ok = True

    def __init__(self, *args: Any, **kwargs: Any):
        """ """
        if "type" not in kwargs:
            raise AttributeError(
                "Provide 'type' kwarg inherited from BaseModel or List of BaseModel or UnionType"
            )

        self.__type = kwargs.pop("type")
        self.__ensure_ascii = kwargs.pop("ensure_ascii", False)

        super().__init__(*args, **kwargs)

    def process_result_value(self, value: Any, dialect: Dialect) -> Any:
        if value is None:
            return None
        return parse_obj_as(self.__type, value)

    @staticmethod
    def __pydantic_model_to_json(model: BaseModel, ensure_ascii: bool) -> str:
        return model.json(by_alias=True, exclude_none=True, ensure_ascii=ensure_ascii)

    def serialize(
        self, value: Optional[Union[Dict[Any, Any], List[BaseModel], BaseModel]]
    ) -> Any:
        if value is None:
            return None

        if isinstance(value, list):
            values = [
                self.__pydantic_model_to_json(v, self.__ensure_ascii)
                for v in parse_obj_as(self.__type, value)
            ]
            return f"[{','.join(values)}]"

        return self.__pydantic_model_to_json(
            parse_obj_as(self.__type, value), self.__ensure_ascii
        )

    def bind_processor(self, dialect: Dialect) -> Optional[Any]:
        string_process = self._str_impl.bind_processor(dialect)

        return self._make_bind_processor(string_process, self.serialize)
