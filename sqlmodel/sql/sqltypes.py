from typing import Any, cast

from sqlalchemy import Uuid, types
from sqlalchemy.engine.interfaces import Dialect
from sqlmodel._compat import IS_PYDANTIC_V2
from typing_extensions import deprecated

if IS_PYDANTIC_V2:
    from .pydantic_v2_json import PydanticJSONv2 as PydanticJSON
else:
    from .pydantic_v1_json import PydanticJSONv1 as PydanticJSON  # type: ignore

PydanticJSONType = PydanticJSON


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> types.TypeEngine[Any]:
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)


@deprecated("SQlAlchemy V2 has native support of UUID type - sa.Uuid")
class GUID(Uuid):  # type: ignore
    pass
