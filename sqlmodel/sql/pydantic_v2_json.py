from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, TypeAdapter
from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect


class PydanticJSONv2(types.TypeDecorator):  # type: ignore
    """Type to store Pydantic models as JSON data at database"""

    impl = types.JSON
    cache_ok = False

    def __init__(self, *args: Any, **kwargs: Any):
        """ """
        if "type" not in kwargs:
            raise AttributeError(
                "Provide 'type' kwarg inherited from BaseModel or List of BaseModel or UnionType"
            )

        self._type = TypeAdapter(kwargs.pop("type"))

        super().__init__(*args, **kwargs)

    def process_result_value(self, value: Any, dialect: Dialect) -> Any:
        if value is None:
            return None

        return self._type.validate_python(value)

    def serialize(
        self, value: Optional[Union[Dict[Any, Any], List[BaseModel], BaseModel]]
    ) -> Optional[str]:
        if value is None:
            return None

        return self._type.dump_json(
            self._type.validate_python(value), by_alias=True, exclude_none=True
        ).decode()

    def bind_processor(self, dialect: Dialect) -> Optional[Any]:
        string_process = self._str_impl.bind_processor(dialect)

        return self._make_bind_processor(string_process, self.serialize)
