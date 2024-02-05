from typing import Any, Optional

from pydantic import TypeAdapter
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

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        return self._type.dump_json(
            self._type.validate_python(value), by_alias=True, exclude_none=True
        ).decode()

    def process_result_value(self, value: Any, dialect: Dialect) -> Any:
        if value is None:
            return None

        return self._type.validate_json(value)
