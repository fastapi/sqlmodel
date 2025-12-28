import sys
import types
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ForwardRef,
    Optional,
    TypeVar,
    Union,
)

from annotated_types import MaxLen
from pydantic import VERSION as P_VERSION
from pydantic import BaseModel
from pydantic import ConfigDict as ConfigDict
from pydantic._internal._fields import PydanticMetadata
from pydantic._internal._model_construction import ModelMetaclass as ModelMetaclass
from pydantic._internal._repr import Representation as Representation
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined as Undefined
from pydantic_core import PydanticUndefinedType as PydanticUndefinedType
from typing_extensions import get_args, get_origin

BaseConfig = ConfigDict
UndefinedType = PydanticUndefinedType
PYDANTIC_MINOR_VERSION = tuple(int(i) for i in P_VERSION.split(".")[:2])


if TYPE_CHECKING:
    from .main import RelationshipInfo, SQLModel

UnionType = getattr(types, "UnionType", Union)
NoneType = type(None)
T = TypeVar("T")
InstanceOrType = Union[T, type[T]]
_TSQLModel = TypeVar("_TSQLModel", bound="SQLModel")


class FakeMetadata:
    max_length: Optional[int] = None
    max_digits: Optional[int] = None
    decimal_places: Optional[int] = None


@dataclass
class ObjectWithUpdateWrapper:
    obj: Any
    update: dict[str, Any]

    def __getattribute__(self, __name: str) -> Any:
        update = super().__getattribute__("update")
        obj = super().__getattribute__("obj")
        if __name in update:
            return update[__name]
        return getattr(obj, __name)


def _is_union_type(t: Any) -> bool:
    return t is UnionType or t is Union


finish_init: ContextVar[bool] = ContextVar("finish_init", default=True)


@contextmanager
def partial_init() -> Generator[None, None, None]:
    token = finish_init.set(False)
    yield
    finish_init.reset(token)


class SQLModelConfig(BaseConfig, total=False):
    table: Optional[bool]
    registry: Optional[Any]


def get_model_fields(model: InstanceOrType[BaseModel]) -> dict[str, "FieldInfo"]:
    # TODO: refactor the usage of this function to always pass the class
    # not the instance, and then remove this extra check
    # this is for compatibility with Pydantic v3
    if isinstance(model, type):
        use_model = model
    else:
        use_model = model.__class__
    return use_model.model_fields


def init_pydantic_private_attrs(new_object: InstanceOrType["SQLModel"]) -> None:
    object.__setattr__(new_object, "__pydantic_fields_set__", set())
    object.__setattr__(new_object, "__pydantic_extra__", None)
    object.__setattr__(new_object, "__pydantic_private__", None)


def get_annotations(class_dict: dict[str, Any]) -> dict[str, Any]:
    raw_annotations: dict[str, Any] = class_dict.get("__annotations__", {})
    if sys.version_info >= (3, 14) and "__annotations__" not in class_dict:
        # See https://github.com/pydantic/pydantic/pull/11991
        from annotationlib import (
            Format,
            call_annotate_function,
            get_annotate_from_class_namespace,
        )

        if annotate := get_annotate_from_class_namespace(class_dict):
            raw_annotations = call_annotate_function(annotate, format=Format.FORWARDREF)
    return raw_annotations


def is_table_model_class(cls: type[Any]) -> bool:
    config = getattr(cls, "model_config", {})
    if config:
        return config.get("table", False) or False
    return False


def get_relationship_to(
    name: str,
    rel_info: "RelationshipInfo",
    annotation: Any,
) -> Any:
    origin = get_origin(annotation)
    use_annotation = annotation
    # Direct relationships (e.g. 'Team' or Team) have None as an origin
    if origin is None:
        if isinstance(use_annotation, ForwardRef):
            use_annotation = use_annotation.__forward_arg__
        else:
            return use_annotation
    # If Union (e.g. Optional), get the real field
    elif _is_union_type(origin):
        use_annotation = get_args(annotation)
        if len(use_annotation) > 2:
            raise ValueError("Cannot have a (non-optional) union as a SQLAlchemy field")
        arg1, arg2 = use_annotation
        if arg1 is NoneType and arg2 is not NoneType:
            use_annotation = arg2
        elif arg2 is NoneType and arg1 is not NoneType:
            use_annotation = arg1
        else:
            raise ValueError(
                "Cannot have a Union of None and None as a SQLAlchemy field"
            )

    # If a list, then also get the real field
    elif origin is list:
        use_annotation = get_args(annotation)[0]

    return get_relationship_to(name=name, rel_info=rel_info, annotation=use_annotation)


def is_field_noneable(field: "FieldInfo") -> bool:
    if getattr(field, "nullable", Undefined) is not Undefined:
        return field.nullable  # type: ignore
    origin = get_origin(field.annotation)
    if origin is not None and _is_union_type(origin):
        args = get_args(field.annotation)
        if any(arg is NoneType for arg in args):
            return True
    if not field.is_required():
        if field.default is Undefined:
            return False
        if field.annotation is None or field.annotation is NoneType:
            return True
        return False
    return False


def get_sa_type_from_type_annotation(annotation: Any) -> Any:
    # Resolve Optional fields
    if annotation is None:
        raise ValueError("Missing field type")
    origin = get_origin(annotation)
    if origin is None:
        return annotation
    elif origin is Annotated:
        return get_sa_type_from_type_annotation(get_args(annotation)[0])
    if _is_union_type(origin):
        bases = get_args(annotation)
        if len(bases) > 2:
            raise ValueError("Cannot have a (non-optional) union as a SQLAlchemy field")
        # Non optional unions are not allowed
        if bases[0] is not NoneType and bases[1] is not NoneType:
            raise ValueError("Cannot have a (non-optional) union as a SQLAlchemy field")
        # Optional unions are allowed
        use_type = bases[0] if bases[0] is not NoneType else bases[1]
        return get_sa_type_from_type_annotation(use_type)
    return origin


def get_sa_type_from_field(field: Any) -> Any:
    type_: Any = field.annotation
    return get_sa_type_from_type_annotation(type_)


def get_field_metadata(field: Any) -> Any:
    for meta in field.metadata:
        if isinstance(meta, (PydanticMetadata, MaxLen)):
            return meta
    return FakeMetadata()


def sqlmodel_table_construct(
    *,
    self_instance: _TSQLModel,
    values: dict[str, Any],
    _fields_set: Union[set[str], None] = None,
) -> _TSQLModel:
    # Copy from Pydantic's BaseModel.construct()
    # Ref: https://github.com/pydantic/pydantic/blob/v2.5.2/pydantic/main.py#L198
    # Modified to not include everything, only the model fields, and to
    # set relationships
    # SQLModel override to get class SQLAlchemy __dict__ attributes and
    # set them back in after creating the object
    # new_obj = cls.__new__(cls)
    cls = type(self_instance)
    old_dict = self_instance.__dict__.copy()
    # End SQLModel override

    fields_values: dict[str, Any] = {}
    defaults: dict[
        str, Any
    ] = {}  # keeping this separate from `fields_values` helps us compute `_fields_set`
    for name, field in cls.model_fields.items():
        if field.alias and field.alias in values:
            fields_values[name] = values.pop(field.alias)
        elif name in values:
            fields_values[name] = values.pop(name)
        elif not field.is_required():
            defaults[name] = field.get_default(call_default_factory=True)
    if _fields_set is None:
        _fields_set = set(fields_values.keys())
    fields_values.update(defaults)

    _extra: Union[dict[str, Any], None] = None
    if cls.model_config.get("extra") == "allow":
        _extra = {}
        for k, v in values.items():
            _extra[k] = v
    # SQLModel override, do not include everything, only the model fields
    # else:
    #     fields_values.update(values)
    # End SQLModel override
    # SQLModel override
    # Do not set __dict__, instead use setattr to trigger SQLAlchemy
    # object.__setattr__(new_obj, "__dict__", fields_values)
    # instrumentation
    for key, value in {**old_dict, **fields_values}.items():
        setattr(self_instance, key, value)
    # End SQLModel override
    object.__setattr__(self_instance, "__pydantic_fields_set__", _fields_set)
    if not cls.__pydantic_root_model__:
        object.__setattr__(self_instance, "__pydantic_extra__", _extra)

    if cls.__pydantic_post_init__:
        self_instance.model_post_init(None)
    elif not cls.__pydantic_root_model__:
        # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist
        # Since it doesn't, that means that `__pydantic_private__` should be set to None
        object.__setattr__(self_instance, "__pydantic_private__", None)
    # SQLModel override, set relationships
    # Get and set any relationship objects
    for key in self_instance.__sqlmodel_relationships__:
        value = values.get(key, Undefined)
        if value is not Undefined:
            setattr(self_instance, key, value)
    # End SQLModel override
    return self_instance


def sqlmodel_validate(
    cls: type[_TSQLModel],
    obj: Any,
    *,
    strict: Union[bool, None] = None,
    from_attributes: Union[bool, None] = None,
    context: Union[dict[str, Any], None] = None,
    update: Union[dict[str, Any], None] = None,
) -> _TSQLModel:
    if not is_table_model_class(cls):
        new_obj: _TSQLModel = cls.__new__(cls)
    else:
        # If table, create the new instance normally to make SQLAlchemy create
        # the _sa_instance_state attribute
        # The wrapper of this function should use with _partial_init()
        with partial_init():
            new_obj = cls()
    # SQLModel Override to get class SQLAlchemy __dict__ attributes and
    # set them back in after creating the object
    old_dict = new_obj.__dict__.copy()
    use_obj = obj
    if isinstance(obj, dict) and update:
        use_obj = {**obj, **update}
    elif update:
        use_obj = ObjectWithUpdateWrapper(obj=obj, update=update)
    cls.__pydantic_validator__.validate_python(
        use_obj,
        strict=strict,
        from_attributes=from_attributes,
        context=context,
        self_instance=new_obj,
    )
    # Capture fields set to restore it later
    fields_set = new_obj.__pydantic_fields_set__.copy()
    if not is_table_model_class(cls):
        # If not table, normal Pydantic code, set __dict__
        new_obj.__dict__ = {**old_dict, **new_obj.__dict__}
    else:
        # Do not set __dict__, instead use setattr to trigger SQLAlchemy
        # instrumentation
        for key, value in {**old_dict, **new_obj.__dict__}.items():
            setattr(new_obj, key, value)
    # Restore fields set
    object.__setattr__(new_obj, "__pydantic_fields_set__", fields_set)
    # Get and set any relationship objects
    if is_table_model_class(cls):
        for key in new_obj.__sqlmodel_relationships__:
            value = getattr(use_obj, key, Undefined)
            if value is not Undefined:
                setattr(new_obj, key, value)
    return new_obj


def sqlmodel_init(*, self: "SQLModel", data: dict[str, Any]) -> None:
    old_dict = self.__dict__.copy()
    if not is_table_model_class(self.__class__):
        self.__pydantic_validator__.validate_python(
            data,
            self_instance=self,
        )
    else:
        sqlmodel_table_construct(
            self_instance=self,
            values=data,
        )
    object.__setattr__(
        self,
        "__dict__",
        {**old_dict, **self.__dict__},
    )
