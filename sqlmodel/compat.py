import ipaddress
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from types import NoneType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    ForwardRef,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from pydantic import VERSION as PYDANTIC_VERSION
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    Numeric,
)
from sqlalchemy import Enum as sa_Enum
from sqlalchemy.sql.sqltypes import LargeBinary, Time

from .sql.sqltypes import GUID, AutoString

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict as PydanticModelConfig
    from pydantic._internal._fields import PydanticMetadata
    from pydantic._internal._model_construction import ModelMetaclass
    from pydantic_core import PydanticUndefined as Undefined  # noqa
    from pydantic_core import PydanticUndefinedType as UndefinedType

    # Dummy for types, to make it importable
    class ModelField:
        pass
else:
    from pydantic import BaseConfig as PydanticModelConfig
    from pydantic.fields import SHAPE_SINGLETON, ModelField
    from pydantic.fields import Undefined as Undefined  # noqa
    from pydantic.fields import UndefinedType as UndefinedType
    from pydantic.main import ModelMetaclass as ModelMetaclass
    from pydantic.typing import resolve_annotations

if TYPE_CHECKING:
    from .main import FieldInfo, RelationshipInfo, SQLModel, SQLModelMetaclass


NoArgAnyCallable = Callable[[], Any]
T = TypeVar("T")
InstanceOrType = Union[T, Type[T]]

if IS_PYDANTIC_V2:

    class SQLModelConfig(PydanticModelConfig, total=False):
        table: Optional[bool]
        registry: Optional[Any]

else:

    class SQLModelConfig(PydanticModelConfig):
        table: Optional[bool] = None
        registry: Optional[Any] = None


def get_model_config(model: type) -> Optional[SQLModelConfig]:
    if IS_PYDANTIC_V2:
        return getattr(model, "model_config", None)
    else:
        return getattr(model, "__config__", None)


def get_config_value(
    model: InstanceOrType["SQLModel"], parameter: str, default: Any = None
) -> Any:
    if IS_PYDANTIC_V2:
        return model.model_config.get(parameter, default)
    else:
        return getattr(model.__config__, parameter, default)


def set_config_value(
    model: InstanceOrType["SQLModel"],
    parameter: str,
    value: Any,
    v1_parameter: Optional[str] = None,
) -> None:
    if IS_PYDANTIC_V2:
        model.model_config[parameter] = value  # type: ignore
    else:
        setattr(model.__config__, v1_parameter or parameter, value)  # type: ignore


def get_model_fields(model: InstanceOrType["SQLModel"]) -> Dict[str, "FieldInfo"]:
    if IS_PYDANTIC_V2:
        return model.model_fields  # type: ignore
    else:
        return model.__fields__  # type: ignore


def get_fields_set(model: InstanceOrType["SQLModel"]) -> set[str]:
    if IS_PYDANTIC_V2:
        return model.__pydantic_fields_set__  # type: ignore
    else:
        return model.__fields_set__  # type: ignore


def set_fields_set(
    new_object: InstanceOrType["SQLModel"], fields: set["FieldInfo"]
) -> None:
    if IS_PYDANTIC_V2:
        object.__setattr__(new_object, "__pydantic_fields_set__", fields)
    else:
        object.__setattr__(new_object, "__fields_set__", fields)


def set_attribute_mode(cls: Type["SQLModelMetaclass"]) -> None:
    if IS_PYDANTIC_V2:
        cls.model_config["read_from_attributes"] = True
    else:
        cls.__config__.read_with_orm_mode = True  # type: ignore


def get_annotations(class_dict: dict[str, Any]) -> dict[str, Any]:
    if IS_PYDANTIC_V2:
        return class_dict.get("__annotations__", {})
    else:
        return resolve_annotations(
            class_dict.get("__annotations__", {}), class_dict.get("__module__", None)
        )


def class_dict_is_table(
    class_dict: dict[str, Any], class_kwargs: dict[str, Any]
) -> bool:
    config: SQLModelConfig = {}
    if IS_PYDANTIC_V2:
        config = class_dict.get("model_config", {})
    else:
        config = class_dict.get("__config__", {})
    config_table = config.get("table", Undefined)
    if config_table is not Undefined:
        return config_table  # type: ignore
    kw_table = class_kwargs.get("table", Undefined)
    if kw_table is not Undefined:
        return kw_table  # type: ignore
    return False


def cls_is_table(cls: Type) -> bool:
    if IS_PYDANTIC_V2:
        config = getattr(cls, "model_config", None)
        if not config:
            return False
        return config.get("table", False)
    else:
        config = getattr(cls, "__config__", None)
        if not config:
            return False
        return getattr(config, "table", False)


def get_relationship_to(
    name: str,
    rel_info: "RelationshipInfo",
    annotation: Any,
) -> Any:
    if IS_PYDANTIC_V2:
        # TODO: review rename origin and relationship_to
        relationship_to = get_origin(annotation)
        # Direct relationships (e.g. 'Team' or Team) have None as an origin
        if relationship_to is None:
            relationship_to = annotation
        # If Union (e.g. Optional), get the real field
        elif relationship_to is Union:
            relationship_to = get_args(annotation)[0]
        # If a list, then also get the real field
        elif relationship_to is list:
            relationship_to = get_args(annotation)[0]
        # TODO: given this, should there be a recursive call in this whole if block to get_relationship_to?
        if isinstance(relationship_to, ForwardRef):
            relationship_to = relationship_to.__forward_arg__
        return relationship_to
    else:
        temp_field = ModelField.infer(
            name=name,
            value=rel_info,
            annotation=annotation,
            class_validators=None,
            config=SQLModelConfig,
        )
        relationship_to = temp_field.type_
        if isinstance(temp_field.type_, ForwardRef):
            relationship_to = temp_field.type_.__forward_arg__
        return relationship_to


def set_empty_defaults(annotations: Dict[str, Any], class_dict: Dict[str, Any]) -> None:
    """
    Pydantic v2 without required fields with no optionals cannot do empty initialisations.
    This means we cannot do Table() and set fields later.
    We go around this by adding a default to everything, being None

    Args:
        annotations: Dict[str, Any]: The annotations to provide to pydantic
        class_dict: Dict[str, Any]: The class dict for the defaults
    """
    # TODO: no v1?
    if IS_PYDANTIC_V2:
        from .main import FieldInfo

        # Pydantic v2 sets a __pydantic_core_schema__ which is very hard to change. Changing the fields does not do anything
        for key in annotations.keys():
            value = class_dict.get(key, Undefined)
            if value is Undefined:
                class_dict[key] = None
            elif isinstance(value, FieldInfo):
                if (
                    value.default in (Undefined, Ellipsis)
                ) and value.default_factory is None:
                    # So we can check for nullable
                    value.default = None


def _is_field_noneable(field: "FieldInfo") -> bool:
    if IS_PYDANTIC_V2:
        if getattr(field, "nullable", Undefined) is not Undefined:
            return field.nullable  # type: ignore
        if not field.is_required():
            if field.default is Undefined:
                return False
            if field.annotation is None or field.annotation is NoneType:
                return True
            if get_origin(field.annotation) is Union:
                for base in get_args(field.annotation):
                    if base is NoneType:
                        return True
            return False
        return False
    else:
        if not field.required:
            # Taken from [Pydantic](https://github.com/samuelcolvin/pydantic/blob/v1.8.2/pydantic/fields.py#L946-L947)
            return field.allow_none and (
                field.shape != SHAPE_SINGLETON or not field.sub_fields
            )
        return field.allow_none


def get_sqlalchemy_type(field: Any) -> Any:
    if IS_PYDANTIC_V2:
        field_info = field
    else:
        field_info = field.field_info
    sa_type = getattr(field_info, "sa_type", Undefined)  # noqa: B009
    if sa_type is not Undefined:
        return sa_type

    type_ = get_type_from_field(field)
    metadata = get_field_metadata(field)

    # Check enums first as an enum can also be a str, needed by Pydantic/FastAPI
    if issubclass(type_, Enum):
        return sa_Enum(type_)
    if issubclass(type_, str):
        max_length = getattr(metadata, "max_length", None)
        if max_length:
            return AutoString(length=max_length)
        return AutoString
    if issubclass(type_, float):
        return Float
    if issubclass(type_, bool):
        return Boolean
    if issubclass(type_, int):
        return Integer
    if issubclass(type_, datetime):
        return DateTime
    if issubclass(type_, date):
        return Date
    if issubclass(type_, timedelta):
        return Interval
    if issubclass(type_, time):
        return Time
    if issubclass(type_, bytes):
        return LargeBinary
    if issubclass(type_, Decimal):
        return Numeric(
            precision=getattr(metadata, "max_digits", None),
            scale=getattr(metadata, "decimal_places", None),
        )
    if issubclass(type_, ipaddress.IPv4Address):
        return AutoString
    if issubclass(type_, ipaddress.IPv4Network):
        return AutoString
    if issubclass(type_, ipaddress.IPv6Address):
        return AutoString
    if issubclass(type_, ipaddress.IPv6Network):
        return AutoString
    if issubclass(type_, Path):
        return AutoString
    if issubclass(type_, uuid.UUID):
        return GUID
    raise ValueError(f"{type_} has no matching SQLAlchemy type")


def get_type_from_field(field: Any) -> type:
    if IS_PYDANTIC_V2:
        type_: type | None = field.annotation
        # Resolve Optional fields
        if type_ is None:
            raise ValueError("Missing field type")
        origin = get_origin(type_)
        if origin is None:
            return type_
        if origin is Union:
            bases = get_args(type_)
            if len(bases) > 2:
                raise ValueError(
                    "Cannot have a (non-optional) union as a SQL alchemy field"
                )
            # Non optional unions are not allowed
            if bases[0] is not NoneType and bases[1] is not NoneType:
                raise ValueError(
                    "Cannot have a (non-optional) union as a SQL alchemy field"
                )
            # Optional unions are allowed
            return bases[0] if bases[0] is not NoneType else bases[1]
        return origin
    else:
        if isinstance(field.type_, type) and field.shape == SHAPE_SINGLETON:
            return field.type_
        raise ValueError(f"The field {field.name} has no matching SQLAlchemy type")


class FakeMetadata:
    max_length: Optional[int] = None
    max_digits: Optional[int] = None
    decimal_places: Optional[int] = None


def get_field_metadata(field: Any) -> Any:
    if IS_PYDANTIC_V2:
        for meta in field.metadata:
            if isinstance(meta, PydanticMetadata):
                return meta
        return FakeMetadata()
    else:
        metadata = FakeMetadata()
        metadata.max_length = field.field_info.max_length
        metadata.max_digits = getattr(field.type_, "max_digits", None)
        metadata.decimal_places = getattr(field.type_, "decimal_places", None)
        return metadata


def get_column_from_field(field: Any) -> Column:  # type: ignore
    if IS_PYDANTIC_V2:
        field_info = field
    else:
        field_info = field.field_info
    sa_column = getattr(field_info, "sa_column", Undefined)
    if isinstance(sa_column, Column):
        return sa_column
    sa_type = get_sqlalchemy_type(field)
    primary_key = getattr(field_info, "primary_key", Undefined)
    if primary_key is Undefined:
        primary_key = False
    index = getattr(field_info, "index", Undefined)
    if index is Undefined:
        index = False
    nullable = not primary_key and _is_field_noneable(field)
    # Override derived nullability if the nullable property is set explicitly
    # on the field
    field_nullable = getattr(field_info, "nullable", Undefined)  # noqa: B009
    if field_nullable is not Undefined:
        assert not isinstance(field_nullable, UndefinedType)
        nullable = field_nullable
    args = []
    foreign_key = getattr(field_info, "foreign_key", Undefined)
    if foreign_key is Undefined:
        foreign_key = None
    unique = getattr(field_info, "unique", Undefined)
    if unique is Undefined:
        unique = False
    if foreign_key:
        assert isinstance(foreign_key, str)
        args.append(ForeignKey(foreign_key))
    kwargs = {
        "primary_key": primary_key,
        "nullable": nullable,
        "index": index,
        "unique": unique,
    }
    sa_default = Undefined
    if field_info.default_factory:
        sa_default = field_info.default_factory
    elif field_info.default is not Undefined:
        sa_default = field_info.default
    if sa_default is not Undefined:
        kwargs["default"] = sa_default
    sa_column_args = getattr(field_info, "sa_column_args", Undefined)
    if sa_column_args is not Undefined:
        args.extend(list(cast(Sequence[Any], sa_column_args)))
    sa_column_kwargs = getattr(field_info, "sa_column_kwargs", Undefined)
    if sa_column_kwargs is not Undefined:
        kwargs.update(cast(Dict[Any, Any], sa_column_kwargs))
    return Column(sa_type, *args, **kwargs)  # type: ignore


def post_init_field_info(field_info: FieldInfo) -> None:
    if not IS_PYDANTIC_V2:
        field_info._validate()
