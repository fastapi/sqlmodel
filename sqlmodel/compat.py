from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
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

IS_PYDANTIC_V2 = int(PYDANTIC_VERSION.split(".")[0]) >= 2


if IS_PYDANTIC_V2:
    from pydantic import ConfigDict
    from pydantic_core import PydanticUndefined as PydanticUndefined, PydanticUndefinedType as PydanticUndefinedType # noqa
else:
    from pydantic import BaseConfig # noqa
    from pydantic.fields import ModelField # noqa
    from pydantic.fields import Undefined as PydanticUndefined, UndefinedType as PydanticUndefinedType # noqa

if TYPE_CHECKING:
    from .main import FieldInfo, RelationshipInfo, SQLModel, SQLModelMetaclass


NoArgAnyCallable = Callable[[], Any]
T = TypeVar("T")
InstanceOrType = Union[T, Type[T]]

if IS_PYDANTIC_V2:

    class SQLModelConfig(ConfigDict, total=False):
        table: Optional[bool]
        read_from_attributes: Optional[bool]
        registry: Optional[Any]

else:

    class SQLModelConfig(BaseConfig):
        table: Optional[bool] = None
        read_from_attributes: Optional[bool] = None
        registry: Optional[Any] = None

        def __getitem__(self, item: str) -> Any:
            return self.__getattr__(item)

        def __setitem__(self, item: str, value: Any) -> None:
            return self.__setattr__(item, value)


# Inspired from https://github.com/roman-right/beanie/blob/main/beanie/odm/utils/pydantic.py
def get_model_config(model: type) -> Optional[SQLModelConfig]:
    if IS_PYDANTIC_V2:
        return getattr(model, "model_config", None)
    else:
        return getattr(model, "Config", None)


def get_config_value(
    model: InstanceOrType["SQLModel"], parameter: str, default: Any = None
) -> Any:
    if IS_PYDANTIC_V2:
        return model.model_config.get(parameter, default)
    else:
        return getattr(model.Config, parameter, default)


def set_config_value(
    model: InstanceOrType["SQLModel"], parameter: str, value: Any, v1_parameter: str = None
) -> None:
    if IS_PYDANTIC_V2:
        model.model_config[parameter] = value # type: ignore
    else:
        model.Config[v1_parameter or parameter] = value  # type: ignore


def get_model_fields(model: InstanceOrType["SQLModel"]) -> Dict[str, "FieldInfo"]:
    if IS_PYDANTIC_V2:
        return model.model_fields # type: ignore
    else:
        return model.__fields__ # type: ignore


def get_fields_set(model: InstanceOrType["SQLModel"]) -> set[str]:
    if IS_PYDANTIC_V2:
        return model.__pydantic_fields_set__
    else:
        return model.__fields_set__ # type: ignore


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
        cls.__config__.read_with_orm_mode = True # type: ignore


def get_relationship_to(
    name: str,
    rel_info: "RelationshipInfo",
    annotation: Any,
) -> Any:
    if IS_PYDANTIC_V2:
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
    if IS_PYDANTIC_V2:
        from .main import FieldInfo
        # Pydantic v2 sets a __pydantic_core_schema__ which is very hard to change. Changing the fields does not do anything
        for key in annotations.keys():
            value = class_dict.get(key, PydanticUndefined)
            if value is PydanticUndefined:
                class_dict[key] = None
            elif isinstance(value, FieldInfo):
                if (
                    value.default in (PydanticUndefined, Ellipsis)
                ) and value.default_factory is None:
                    # So we can check for nullable
                    value.original_default = value.default  
                    value.default = None
