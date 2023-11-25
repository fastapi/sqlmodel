from types import NoneType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    ForwardRef,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from pydantic import VERSION as PYDANTIC_VERSION

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict as BaseConfig
    from pydantic._internal._fields import PydanticMetadata
    from pydantic._internal._model_construction import ModelMetaclass
    from pydantic_core import PydanticUndefined as Undefined  # noqa
    from pydantic_core import PydanticUndefinedType as UndefinedType

    # Dummy for types, to make it importable
    class ModelField:
        pass
else:
    from pydantic import BaseConfig as BaseConfig
    from pydantic.fields import SHAPE_SINGLETON, ModelField
    from pydantic.fields import Undefined as Undefined  # noqa
    from pydantic.fields import UndefinedType as UndefinedType
    from pydantic.main import ModelMetaclass as ModelMetaclass
    from pydantic.typing import resolve_annotations

if TYPE_CHECKING:
    from .main import FieldInfo, RelationshipInfo, SQLModel


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


def get_config_value(
    *, model: InstanceOrType["SQLModel"], parameter: str, default: Any = None
) -> Any:
    if IS_PYDANTIC_V2:
        return model.model_config.get(parameter, default)
    else:
        return getattr(model.__config__, parameter, default)


def set_config_value(
    *,
    model: InstanceOrType["SQLModel"],
    parameter: str,
    value: Any,
) -> None:
    if IS_PYDANTIC_V2:
        model.model_config[parameter] = value  # type: ignore
    else:
        setattr(model.__config__, parameter, value)  # type: ignore


def get_model_fields(model: InstanceOrType["SQLModel"]) -> Dict[str, "FieldInfo"]:
    if IS_PYDANTIC_V2:
        return model.model_fields  # type: ignore
    else:
        return model.__fields__  # type: ignore


def set_fields_set(
    new_object: InstanceOrType["SQLModel"], fields: set["FieldInfo"]
) -> None:
    if IS_PYDANTIC_V2:
        object.__setattr__(new_object, "__pydantic_fields_set__", fields)
    else:
        object.__setattr__(new_object, "__fields_set__", fields)


def get_annotations(class_dict: dict[str, Any]) -> dict[str, Any]:
    if IS_PYDANTIC_V2:
        return class_dict.get("__annotations__", {})
    else:
        return resolve_annotations(
            class_dict.get("__annotations__", {}), class_dict.get("__module__", None)
        )

# TODO: review if this is necessary
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
                    "Cannot have a (non-optional) union as a SQLAlchemy field"
                )
            # Non optional unions are not allowed
            if bases[0] is not NoneType and bases[1] is not NoneType:
                raise ValueError(
                    "Cannot have a (non-optional) union as a SQLlchemy field"
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


def post_init_field_info(field_info: FieldInfo) -> None:
    if not IS_PYDANTIC_V2:
        field_info._validate()
