from __future__ import annotations

import ipaddress
import uuid
import weakref
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from google.protobuf.descriptor import Descriptor
from google.protobuf.message import Message
from google.protobuf import json_format as _pb_json_format
from google.protobuf import struct_pb2 as _pb_struct_pb2
from google.protobuf import message as _pb_message_mod
from google.protobuf import descriptor_pb2 as _pb_desc_pb2
from google.protobuf import descriptor_pool as _pb_desc_pool
import warnings
from pydantic import BaseModel, EmailStr
from pydantic.fields import FieldInfo as PydanticFieldInfo
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
    inspect,
)
from sqlalchemy import Enum as sa_Enum
from sqlalchemy.orm import (
    Mapped,
    RelationshipProperty,
    declared_attr,
    registry,
    relationship,
)
from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.instrumentation import is_instrumented
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import LargeBinary, Time, Uuid
from typing_extensions import Literal, TypeAlias, deprecated, get_origin

from ._compat import (  # type: ignore[attr-defined]
    IS_PYDANTIC_V2,
    PYDANTIC_MINOR_VERSION,
    BaseConfig,
    ModelField,
    ModelMetaclass,
    Representation,
    SQLModelConfig,
    Undefined,
    UndefinedType,
    _calculate_keys,
    finish_init,
    get_annotations,
    get_config_value,
    get_field_metadata,
    get_model_fields,
    get_relationship_to,
    get_sa_type_from_field,
    init_pydantic_private_attrs,
    is_field_noneable,
    is_table_model_class,
    post_init_field_info,
    set_config_value,
    sqlmodel_init,
    sqlmodel_validate,
)
from .sql.sqltypes import AutoString

if TYPE_CHECKING:
    from pydantic._internal._model_construction import ModelMetaclass as ModelMetaclass
    from pydantic._internal._repr import Representation as Representation
    from pydantic_core import PydanticUndefined as Undefined
    from pydantic_core import PydanticUndefinedType as UndefinedType

_T = TypeVar("_T")
NoArgAnyCallable = Callable[[], Any]
IncEx: TypeAlias = Union[
    Set[int],
    Set[str],
    Mapping[int, Union["IncEx", bool]],
    Mapping[str, Union["IncEx", bool]],
]
OnDeleteType = Literal["CASCADE", "SET NULL", "RESTRICT"]


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    return lambda a: a


class FieldInfo(PydanticFieldInfo):  # type: ignore[misc]
    # mypy - ignore that PydanticFieldInfo is @final
    def __init__(self, default: Any = Undefined, **kwargs: Any) -> None:
        primary_key = kwargs.pop("primary_key", False)
        nullable = kwargs.pop("nullable", Undefined)
        foreign_key = kwargs.pop("foreign_key", Undefined)
        ondelete = kwargs.pop("ondelete", Undefined)
        unique = kwargs.pop("unique", False)
        index = kwargs.pop("index", Undefined)
        sa_type = kwargs.pop("sa_type", Undefined)
        sa_column = kwargs.pop("sa_column", Undefined)
        sa_column_args = kwargs.pop("sa_column_args", Undefined)
        sa_column_kwargs = kwargs.pop("sa_column_kwargs", Undefined)
        grpc_descriptor = kwargs.pop("grpc_descriptor", Undefined)
        if sa_column is not Undefined:
            if sa_column_args is not Undefined:
                raise RuntimeError(
                    "Passing sa_column_args is not supported when "
                    "also passing a sa_column"
                )
            if sa_column_kwargs is not Undefined:
                raise RuntimeError(
                    "Passing sa_column_kwargs is not supported when "
                    "also passing a sa_column"
                )
            if primary_key is not Undefined:
                raise RuntimeError(
                    "Passing primary_key is not supported when also passing a sa_column"
                )
            if nullable is not Undefined:
                raise RuntimeError(
                    "Passing nullable is not supported when also passing a sa_column"
                )
            if foreign_key is not Undefined:
                raise RuntimeError(
                    "Passing foreign_key is not supported when also passing a sa_column"
                )
            if ondelete is not Undefined:
                raise RuntimeError(
                    "Passing ondelete is not supported when also passing a sa_column"
                )
            if unique is not Undefined:
                raise RuntimeError(
                    "Passing unique is not supported when also passing a sa_column"
                )
            if index is not Undefined:
                raise RuntimeError(
                    "Passing index is not supported when also passing a sa_column"
                )
            if sa_type is not Undefined:
                raise RuntimeError(
                    "Passing sa_type is not supported when also passing a sa_column"
                )
        if ondelete is not Undefined:
            if foreign_key is Undefined:
                raise RuntimeError("ondelete can only be used with foreign_key")
        super().__init__(default=default, **kwargs)
        self.primary_key = primary_key
        self.nullable = nullable
        self.foreign_key = foreign_key
        self.ondelete = ondelete
        self.unique = unique
        self.index = index
        self.sa_type = sa_type
        self.sa_column = sa_column
        self.sa_column_args = sa_column_args
        self.sa_column_kwargs = sa_column_kwargs
        self.grpc_descriptor = grpc_descriptor


class RelationshipInfo(Representation):
    def __init__(
        self,
        *,
        back_populates: Optional[str] = None,
        cascade_delete: Optional[bool] = False,
        passive_deletes: Optional[Union[bool, Literal["all"]]] = False,
        link_model: Optional[Any] = None,
        sa_relationship: Optional[RelationshipProperty] = None,  # type: ignore
        sa_relationship_args: Optional[Sequence[Any]] = None,
        sa_relationship_kwargs: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if sa_relationship is not None:
            if sa_relationship_args is not None:
                raise RuntimeError(
                    "Passing sa_relationship_args is not supported when "
                    "also passing a sa_relationship"
                )
            if sa_relationship_kwargs is not None:
                raise RuntimeError(
                    "Passing sa_relationship_kwargs is not supported when "
                    "also passing a sa_relationship"
                )
        self.back_populates = back_populates
        self.cascade_delete = cascade_delete
        self.passive_deletes = passive_deletes
        self.link_model = link_model
        self.sa_relationship = sa_relationship
        self.sa_relationship_args = sa_relationship_args
        self.sa_relationship_kwargs = sa_relationship_kwargs


# include sa_type, sa_column_args, sa_column_kwargs
@overload
def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    include: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    primary_key: Union[bool, UndefinedType] = Undefined,
    foreign_key: Any = Undefined,
    unique: Union[bool, UndefinedType] = Undefined,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
    sa_type: Union[Type[Any], UndefinedType] = Undefined,
    sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
    sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
) -> Any: ...


# When foreign_key is str, include ondelete
# include sa_type, sa_column_args, sa_column_kwargs
@overload
def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    include: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    primary_key: Union[bool, UndefinedType] = Undefined,
    foreign_key: str,
    ondelete: Union[OnDeleteType, UndefinedType] = Undefined,
    unique: Union[bool, UndefinedType] = Undefined,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
    sa_type: Union[Type[Any], UndefinedType] = Undefined,
    sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
    sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
) -> Any: ...


# Include sa_column, don't include
# primary_key
# foreign_key
# ondelete
# unique
# nullable
# index
# sa_type
# sa_column_args
# sa_column_kwargs
@overload
def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    include: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    sa_column: Union[Column[Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
) -> Any: ...


def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    grpc_descriptor: Optional[Any] = None,
    exclude: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    include: Union[
        AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], Any
    ] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    primary_key: Union[bool, UndefinedType] = Undefined,
    foreign_key: Any = Undefined,
    ondelete: Union[OnDeleteType, UndefinedType] = Undefined,
    unique: Union[bool, UndefinedType] = Undefined,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
    sa_type: Union[Type[Any], UndefinedType] = Undefined,
    sa_column: Union[Column, UndefinedType] = Undefined,  # type: ignore
    sa_column_args: Union[Sequence[Any], UndefinedType] = Undefined,
    sa_column_kwargs: Union[Mapping[str, Any], UndefinedType] = Undefined,
    schema_extra: Optional[Dict[str, Any]] = None,
) -> Any:
    current_schema_extra = schema_extra or {}
    field_info = FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        grpc_descriptor=grpc_descriptor,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        primary_key=primary_key,
        foreign_key=foreign_key,
        ondelete=ondelete,
        unique=unique,
        nullable=nullable,
        index=index,
        sa_type=sa_type,
        sa_column=sa_column,
        sa_column_args=sa_column_args,
        sa_column_kwargs=sa_column_kwargs,
        **current_schema_extra,
    )
    post_init_field_info(field_info)
    return field_info


@overload
def Relationship(
    *,
    back_populates: Optional[str] = None,
    cascade_delete: Optional[bool] = False,
    passive_deletes: Optional[Union[bool, Literal["all"]]] = False,
    link_model: Optional[Any] = None,
    sa_relationship_args: Optional[Sequence[Any]] = None,
    sa_relationship_kwargs: Optional[Mapping[str, Any]] = None,
) -> Any: ...


@overload
def Relationship(
    *,
    back_populates: Optional[str] = None,
    cascade_delete: Optional[bool] = False,
    passive_deletes: Optional[Union[bool, Literal["all"]]] = False,
    link_model: Optional[Any] = None,
    sa_relationship: Optional[RelationshipProperty[Any]] = None,
) -> Any: ...


def Relationship(
    *,
    back_populates: Optional[str] = None,
    cascade_delete: Optional[bool] = False,
    passive_deletes: Optional[Union[bool, Literal["all"]]] = False,
    link_model: Optional[Any] = None,
    sa_relationship: Optional[RelationshipProperty[Any]] = None,
    sa_relationship_args: Optional[Sequence[Any]] = None,
    sa_relationship_kwargs: Optional[Mapping[str, Any]] = None,
) -> Any:
    relationship_info = RelationshipInfo(
        back_populates=back_populates,
        cascade_delete=cascade_delete,
        passive_deletes=passive_deletes,
        link_model=link_model,
        sa_relationship=sa_relationship,
        sa_relationship_args=sa_relationship_args,
        sa_relationship_kwargs=sa_relationship_kwargs,
    )
    return relationship_info


@__dataclass_transform__(kw_only_default=True, field_descriptors=(Field, FieldInfo))
class SQLModelMetaclass(ModelMetaclass, DeclarativeMeta):
    __sqlmodel_relationships__: Dict[str, RelationshipInfo]
    model_config: SQLModelConfig
    model_fields: ClassVar[Dict[str, FieldInfo]]
    __config__: Type[SQLModelConfig]
    __fields__: Dict[str, ModelField]  # type: ignore[assignment]

    # Replicate SQLAlchemy
    def __setattr__(cls, name: str, value: Any) -> None:
        if is_table_model_class(cls):
            DeclarativeMeta.__setattr__(cls, name, value)
        else:
            super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        if is_table_model_class(cls):
            DeclarativeMeta.__delattr__(cls, name)
        else:
            super().__delattr__(name)

    # From Pydantic
    def __new__(
        cls,
        name: str,
        bases: Tuple[Type[Any], ...],
        class_dict: Dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        relationships: Dict[str, RelationshipInfo] = {}
        dict_for_pydantic = {}
        original_annotations = get_annotations(class_dict)
        pydantic_annotations = {}
        relationship_annotations = {}
        for k, v in class_dict.items():
            if isinstance(v, RelationshipInfo):
                relationships[k] = v
            else:
                dict_for_pydantic[k] = v
        for k, v in original_annotations.items():
            if k in relationships:
                relationship_annotations[k] = v
            else:
                pydantic_annotations[k] = v
        dict_used = {
            **dict_for_pydantic,
            "__weakref__": None,
            "__sqlmodel_relationships__": relationships,
            "__annotations__": pydantic_annotations,
        }
        # Duplicate logic from Pydantic to filter config kwargs because if they are
        # passed directly including the registry Pydantic will pass them over to the
        # superclass causing an error
        allowed_config_kwargs: Set[str] = {
            key
            for key in dir(BaseConfig)
            if not (
                key.startswith("__") and key.endswith("__")
            )  # skip dunder methods and attributes
        }
        config_kwargs = {
            key: kwargs[key] for key in kwargs.keys() & allowed_config_kwargs
        }
        new_cls = super().__new__(cls, name, bases, dict_used, **config_kwargs)
        new_cls.__annotations__ = {
            **relationship_annotations,
            **pydantic_annotations,
            **new_cls.__annotations__,
        }

        # Descriptor integration: accept provided DESCRIPTOR or synthesize one
        # Only set if not already defined on the class body
        provided_descriptor = class_dict.get("DESCRIPTOR", None)
        try:
            model_fields_map = get_model_fields(new_cls)
        except Exception:
            model_fields_map = {}
        if provided_descriptor is not None:
            # Validate field names present in descriptor against model fields
            desc_fields = {f.name for f in provided_descriptor.fields}
            missing = set(model_fields_map.keys()) - desc_fields
            if missing:
                raise ValueError(
                    f"DESCRIPTOR missing fields: {sorted(missing)} for {new_cls.__name__}"
                )
            setattr(new_cls, "DESCRIPTOR", provided_descriptor)
        else:
            # Synthesize a minimal Descriptor for reflection
            try:
                pool = _pb_desc_pool.Default()
                file_proto = _pb_desc_pb2.FileDescriptorProto()
                file_proto.name = f"{new_cls.__module__}.{new_cls.__name__}.proto"
                # Use module path as package to help namespacing
                file_proto.package = new_cls.__module__
                msg_proto = file_proto.message_type.add()
                msg_proto.name = new_cls.__name__

                used_numbers: Set[int] = set()

                for idx, (fname, finfo) in enumerate(model_fields_map.items(), start=1):
                    field_proto = msg_proto.field.add()
                    field_proto.name = fname
                    # Use provided field descriptor if present to seed number/type
                    if IS_PYDANTIC_V2:
                        provided_fdesc = getattr(finfo, "grpc_descriptor", None)
                        if provided_fdesc is None:
                            extra = getattr(finfo, "json_schema_extra", None)
                            if isinstance(extra, dict):
                                provided_fdesc = extra.get("grpc_descriptor")
                    else:
                        provided_fdesc = getattr(getattr(finfo, "field_info", finfo), "grpc_descriptor", None)
                    seeded_label = False
                    seeded_type = False
                    if provided_fdesc is not None:
                        # number
                        if hasattr(provided_fdesc, "number"):
                            num = int(getattr(provided_fdesc, "number"))
                            if num in used_numbers or num <= 0:
                                raise ValueError(
                                    f"Duplicate/invalid field number {num} for {fname} in {new_cls.__name__}"
                                )
                            field_proto.number = num
                            used_numbers.add(num)
                        # type
                        if hasattr(provided_fdesc, "type"):
                            field_proto.type = int(getattr(provided_fdesc, "type"))
                            seeded_type = True
                        # label
                        if hasattr(provided_fdesc, "label"):
                            field_proto.label = int(getattr(provided_fdesc, "label"))
                            seeded_label = True
                    # Fill reasonable defaults if not set
                    if field_proto.number == 0:
                        num = idx
                        while num in used_numbers:
                            num += 1
                        field_proto.number = num
                        used_numbers.add(num)

                    # Determine optional vs repeated
                    raw_ann = new_cls.__annotations__.get(fname, None)
                    origin = get_origin(raw_ann)
                    is_repeated = False
                    try:
                        from collections.abc import Sequence as _ABCSequence
                        if origin in (list, tuple) or (isinstance(origin, type) and issubclass(origin, _ABCSequence)):
                            is_repeated = True
                    except Exception:
                        pass
                    if not seeded_label:
                        field_proto.label = (
                            _pb_desc_pb2.FieldDescriptorProto.LABEL_REPEATED if is_repeated else _pb_desc_pb2.FieldDescriptorProto.LABEL_OPTIONAL
                        )

                    # Determine type by python annotation
                    ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_STRING
                    try:
                        def _base_of(annotation: Any) -> Any:
                            ann_origin = get_origin(annotation)
                            # Unwrap Annotated[T, ...]
                            if str(ann_origin) == 'typing.Annotated':
                                args = getattr(annotation, "__args__", ())
                                return args[0] if args else None
                            # Optional/Union
                            if ann_origin is Union:
                                args = [t for t in getattr(annotation, "__args__", ()) if t is not type(None)]  # noqa: E721
                                return args[0] if args else None
                            return annotation

                        target_type = raw_ann
                        elem_type = None
                        if is_repeated:
                            args = getattr(raw_ann, "__args__", ())
                            if args:
                                elem_type = _base_of(args[0])
                        base = _base_of(target_type)
                        scalar = elem_type if elem_type is not None else base
                        if scalar in (int,):
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_INT64
                        elif scalar in (float,):
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_DOUBLE
                        elif scalar in (bool,):
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_BOOL
                        elif scalar in (bytes, bytearray):
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_BYTES
                        elif scalar in (str,):
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_STRING
                        else:
                            # Leave as string by default for complex types
                            warnings.warn(
                                f"Falling back to TYPE_STRING for field '{fname}' in {new_cls.__name__}",
                                RuntimeWarning,
                                stacklevel=2,
                            )
                            ftype = _pb_desc_pb2.FieldDescriptorProto.TYPE_STRING
                    except Exception:
                        warnings.warn(
                            f"Could not infer type for field '{fname}' in {new_cls.__name__}; using TYPE_STRING",
                            RuntimeWarning,
                            stacklevel=2,
                        )
                    if not seeded_type:
                        field_proto.type = ftype

                # Register file in pool; ignore if already added
                # Only add if not already present
                try:
                    pool.FindFileByName(file_proto.name)
                except KeyError:
                    pool.Add(file_proto)
                full_name = f"{file_proto.package}.{msg_proto.name}" if file_proto.package else msg_proto.name
                try:
                        desc = pool.FindMessageTypeByName(full_name)
                        setattr(new_cls, "DESCRIPTOR", desc)
                        # Attach resolved field descriptors back to FieldInfo.grpc_descriptor
                        try:
                            fields_by_name = getattr(desc, "fields_by_name", {})
                            for fname, finfo in model_fields_map.items():
                                fdesc = fields_by_name.get(fname)
                                if fdesc is not None:
                                    if IS_PYDANTIC_V2:
                                        setattr(finfo, "grpc_descriptor", fdesc)
                                    else:
                                        target = getattr(finfo, "field_info", finfo)
                                        setattr(target, "grpc_descriptor", fdesc)
                        except Exception:
                            pass
                except Exception:
                    # As a fallback, leave DESCRIPTOR as None
                    setattr(new_cls, "DESCRIPTOR", None)
            except ValueError:
                # Propagate validation errors (e.g., duplicate field numbers)
                raise
            except Exception:
                setattr(new_cls, "DESCRIPTOR", None)

        def get_config(name: str) -> Any:
            config_class_value = get_config_value(
                model=new_cls, parameter=name, default=Undefined
            )
            if config_class_value is not Undefined:
                return config_class_value
            kwarg_value = kwargs.get(name, Undefined)
            if kwarg_value is not Undefined:
                return kwarg_value
            return Undefined

        config_table = get_config("table")
        if config_table is True:
            # If it was passed by kwargs, ensure it's also set in config
            set_config_value(model=new_cls, parameter="table", value=config_table)
            for k, v in get_model_fields(new_cls).items():
                col = get_column_from_field(v)
                setattr(new_cls, k, col)
            # Set a config flag to tell FastAPI that this should be read with a field
            # in orm_mode instead of preemptively converting it to a dict.
            # This could be done by reading new_cls.model_config['table'] in FastAPI, but
            # that's very specific about SQLModel, so let's have another config that
            # other future tools based on Pydantic can use.
            set_config_value(
                model=new_cls, parameter="read_from_attributes", value=True
            )
            # For compatibility with older versions
            # TODO: remove this in the future
            set_config_value(model=new_cls, parameter="read_with_orm_mode", value=True)

        config_registry = get_config("registry")
        if config_registry is not Undefined:
            config_registry = cast(registry, config_registry)
            # If it was passed by kwargs, ensure it's also set in config
            set_config_value(model=new_cls, parameter="registry", value=config_table)
            setattr(new_cls, "_sa_registry", config_registry)  # noqa: B010
            setattr(new_cls, "metadata", config_registry.metadata)  # noqa: B010
            setattr(new_cls, "__abstract__", True)  # noqa: B010
        return new_cls

    # Override SQLAlchemy, allow both SQLAlchemy and plain Pydantic models
    def __init__(
        cls, classname: str, bases: Tuple[type, ...], dict_: Dict[str, Any], **kw: Any
    ) -> None:
        # Only one of the base classes (or the current one) should be a table model
        # this allows FastAPI cloning a SQLModel for the response_model without
        # trying to create a new SQLAlchemy, for a new table, with the same name, that
        # triggers an error
        base_is_table = any(is_table_model_class(base) for base in bases)
        if is_table_model_class(cls) and not base_is_table:
            for rel_name, rel_info in cls.__sqlmodel_relationships__.items():
                if rel_info.sa_relationship:
                    # There's a SQLAlchemy relationship declared, that takes precedence
                    # over anything else, use that and continue with the next attribute
                    setattr(cls, rel_name, rel_info.sa_relationship)  # Fix #315
                    continue
                raw_ann = cls.__annotations__[rel_name]
                origin: Any = get_origin(raw_ann)
                if origin is Mapped:
                    ann = raw_ann.__args__[0]
                else:
                    ann = raw_ann
                    # Plain forward references, for models not yet defined, are not
                    # handled well by SQLAlchemy without Mapped, so, wrap the
                    # annotations in Mapped here
                    cls.__annotations__[rel_name] = Mapped[ann]  # type: ignore[valid-type]
                relationship_to = get_relationship_to(
                    name=rel_name, rel_info=rel_info, annotation=ann
                )
                rel_kwargs: Dict[str, Any] = {}
                if rel_info.back_populates:
                    rel_kwargs["back_populates"] = rel_info.back_populates
                if rel_info.cascade_delete:
                    rel_kwargs["cascade"] = "all, delete-orphan"
                if rel_info.passive_deletes:
                    rel_kwargs["passive_deletes"] = rel_info.passive_deletes
                if rel_info.link_model:
                    ins = inspect(rel_info.link_model)
                    local_table = getattr(ins, "local_table")  # noqa: B009
                    if local_table is None:
                        raise RuntimeError(
                            "Couldn't find the secondary table for "
                            f"model {rel_info.link_model}"
                        )
                    rel_kwargs["secondary"] = local_table
                rel_args: List[Any] = []
                if rel_info.sa_relationship_args:
                    rel_args.extend(rel_info.sa_relationship_args)
                if rel_info.sa_relationship_kwargs:
                    rel_kwargs.update(rel_info.sa_relationship_kwargs)
                rel_value = relationship(relationship_to, *rel_args, **rel_kwargs)
                setattr(cls, rel_name, rel_value)  # Fix #315
            # SQLAlchemy no longer uses dict_
            # Ref: https://github.com/sqlalchemy/sqlalchemy/commit/428ea01f00a9cc7f85e435018565eb6da7af1b77
            # Tag: 1.4.36
            DeclarativeMeta.__init__(cls, classname, bases, dict_, **kw)
        else:
            ModelMetaclass.__init__(cls, classname, bases, dict_, **kw)


def get_sqlalchemy_type(field: Any) -> Any:
    if IS_PYDANTIC_V2:
        field_info = field
    else:
        field_info = field.field_info
    sa_type = getattr(field_info, "sa_type", Undefined)  # noqa: B009
    if sa_type is not Undefined:
        return sa_type

    type_ = get_sa_type_from_field(field)
    metadata = get_field_metadata(field)

    # Check enums first as an enum can also be a str, needed by Pydantic/FastAPI
    if issubclass(type_, Enum):
        return sa_Enum(type_)
    if issubclass(
        type_,
        (
            str,
            ipaddress.IPv4Address,
            ipaddress.IPv4Network,
            ipaddress.IPv6Address,
            ipaddress.IPv6Network,
            Path,
            EmailStr,
        ),
    ):
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
    if issubclass(type_, uuid.UUID):
        return Uuid
    raise ValueError(f"{type_} has no matching SQLAlchemy type")


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
    nullable = not primary_key and is_field_noneable(field)
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
        if field_info.ondelete == "SET NULL" and not nullable:
            raise RuntimeError('ondelete="SET NULL" requires nullable=True')
        assert isinstance(foreign_key, str)
        ondelete = getattr(field_info, "ondelete", Undefined)
        if ondelete is Undefined:
            ondelete = None
        assert isinstance(ondelete, (str, type(None)))  # for typing
        args.append(ForeignKey(foreign_key, ondelete=ondelete))
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


class_registry = weakref.WeakValueDictionary()  # type: ignore

default_registry = registry()

_TSQLModel = TypeVar("_TSQLModel", bound="SQLModel")


class SQLModel(BaseModel, Message, metaclass=SQLModelMetaclass, registry=default_registry):
    # SQLAlchemy needs to set weakref(s), Pydantic will set the other slots values
    __slots__ = ("__weakref__",)
    __tablename__: ClassVar[Union[str, Callable[..., str]]]
    __sqlmodel_relationships__: ClassVar[Dict[str, RelationshipProperty[Any]]]
    __name__: ClassVar[str]
    metadata: ClassVar[MetaData]
    __allow_unmapped__ = True  # https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-step-six
    DESCRIPTOR: ClassVar[Optional[Descriptor]] = None

    if IS_PYDANTIC_V2:
        model_config = SQLModelConfig(from_attributes=True)
    else:

        class Config:
            orm_mode = True

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        new_object = super().__new__(cls)
        # SQLAlchemy doesn't call __init__ on the base class when querying from DB
        # Ref: https://docs.sqlalchemy.org/en/14/orm/constructors.html
        # Set __fields_set__ here, that would have been set when calling __init__
        # in the Pydantic model so that when SQLAlchemy sets attributes that are
        # added (e.g. when querying from DB) to the __fields_set__, this already exists
        init_pydantic_private_attrs(new_object)
        return new_object

    def __init__(__pydantic_self__, **data: Any) -> None:
        # Uses something other than `self` the first arg to allow "self" as a
        # settable attribute

        # SQLAlchemy does very dark black magic and modifies the __init__ method in
        # sqlalchemy.orm.instrumentation._generate_init()
        # so, to make SQLAlchemy work, it's needed to explicitly call __init__ to
        # trigger all the SQLAlchemy logic, it doesn't work using cls.__new__, setting
        # attributes obj.__dict__, etc. The __init__ method has to be called. But
        # there are cases where calling all the default logic is not ideal, e.g.
        # when calling Model.model_validate(), as the validation is done outside
        # of instance creation.
        # At the same time, __init__ is what users would normally call, by creating
        # a new instance, which should have validation and all the default logic.
        # So, to be able to set up the internal SQLAlchemy logic alone without
        # executing the rest, and support things like Model.model_validate(), we
        # use a contextvar to know if we should execute everything.
        if finish_init.get():
            sqlmodel_init(self=__pydantic_self__, data=data)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in {"_sa_instance_state"}:
            self.__dict__[name] = value
            return
        else:
            # Set in SQLAlchemy, before Pydantic to trigger events and updates
            if is_table_model_class(self.__class__) and is_instrumented(self, name):  # type: ignore[no-untyped-call]
                set_attribute(self, name, value)
            # Set in Pydantic model to trigger possible validation changes, only for
            # non relationship values
            if name not in self.__sqlmodel_relationships__:
                super().__setattr__(name, value)

    def __repr_args__(self) -> Sequence[Tuple[Optional[str], Any]]:
        # Don't show SQLAlchemy private attributes
        return [
            (k, v)
            for k, v in super().__repr_args__()
            if not (isinstance(k, str) and k.startswith("_sa_"))
        ]

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def model_validate(  # type: ignore[override]
        cls: Type[_TSQLModel],
        obj: Any,
        *,
        strict: Union[bool, None] = None,
        from_attributes: Union[bool, None] = None,
        context: Union[Dict[str, Any], None] = None,
        update: Union[Dict[str, Any], None] = None,
    ) -> _TSQLModel:
        return sqlmodel_validate(
            cls=cls,
            obj=obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            update=update,
        )

    def model_dump(
        self,
        *,
        mode: Union[Literal["json", "python"], str] = "python",
        include: Union[IncEx, None] = None,
        exclude: Union[IncEx, None] = None,
        context: Union[Any, None] = None,  # v2.7
        by_alias: Union[bool, None] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,  # v2.12
        round_trip: bool = False,
        warnings: Union[bool, Literal["none", "warn", "error"]] = True,
        fallback: Union[Callable[[Any], Any], None] = None,  # v2.11
        serialize_as_any: bool = False,  # v2.7
    ) -> Dict[str, Any]:
        if PYDANTIC_MINOR_VERSION < (2, 11):
            by_alias = by_alias or False
        extra_kwargs: Dict[str, Any] = {}
        if PYDANTIC_MINOR_VERSION >= (2, 7):
            extra_kwargs["context"] = context
            extra_kwargs["serialize_as_any"] = serialize_as_any
        if PYDANTIC_MINOR_VERSION >= (2, 11):
            extra_kwargs["fallback"] = fallback
        if PYDANTIC_MINOR_VERSION >= (2, 12):
            extra_kwargs["exclude_computed_fields"] = exclude_computed_fields
        if IS_PYDANTIC_V2:
            return super().model_dump(
                mode=mode,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                round_trip=round_trip,
                warnings=warnings,
                **extra_kwargs,
            )
        else:
            return super().dict(
                include=include,
                exclude=exclude,
                by_alias=by_alias or False,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )

    @deprecated(
        """
        🚨 `obj.dict()` was deprecated in SQLModel 0.0.14, you should
        instead use `obj.model_dump()`.
        """
    )
    def dict(
        self,
        *,
        include: Union[IncEx, None] = None,
        exclude: Union[IncEx, None] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return self.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    @classmethod
    @deprecated(
        """
        🚨 `obj.from_orm(data)` was deprecated in SQLModel 0.0.14, you should
        instead use `obj.model_validate(data)`.
        """
    )
    def from_orm(
        cls: Type[_TSQLModel], obj: Any, update: Optional[Dict[str, Any]] = None
    ) -> _TSQLModel:
        return cls.model_validate(obj, update=update)

    @classmethod
    @deprecated(
        """
        🚨 `obj.parse_obj(data)` was deprecated in SQLModel 0.0.14, you should
        instead use `obj.model_validate(data)`.
        """
    )
    def parse_obj(
        cls: Type[_TSQLModel], obj: Any, update: Optional[Dict[str, Any]] = None
    ) -> _TSQLModel:
        if not IS_PYDANTIC_V2:
            obj = cls._enforce_dict_if_root(obj)  # type: ignore[attr-defined] # noqa
        return cls.model_validate(obj, update=update)

    # From Pydantic, override to only show keys from fields, omit SQLAlchemy attributes
    @deprecated(
        """
        🚨 You should not access `obj._calculate_keys()` directly.

        It is only useful for Pydantic v1.X, you should probably upgrade to
        Pydantic v2.X.
        """,
        category=None,
    )
    def _calculate_keys(
        self,
        include: Optional[Mapping[Union[int, str], Any]],
        exclude: Optional[Mapping[Union[int, str], Any]],
        exclude_unset: bool,
        update: Optional[Dict[str, Any]] = None,
    ) -> Optional[AbstractSet[str]]:
        return _calculate_keys(
            self,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            update=update,
        )

    def sqlmodel_update(
        self: _TSQLModel,
        obj: Union[Dict[str, Any], BaseModel],
        *,
        update: Union[Dict[str, Any], None] = None,
    ) -> _TSQLModel:
        use_update = (update or {}).copy()
        if isinstance(obj, dict):
            for key, value in {**obj, **use_update}.items():
                if key in get_model_fields(self):
                    setattr(self, key, value)
        elif isinstance(obj, BaseModel):
            for key in get_model_fields(obj):
                if key in use_update:
                    value = use_update.pop(key)
                else:
                    value = getattr(obj, key)
                setattr(self, key, value)
            for remaining_key in use_update:
                if remaining_key in get_model_fields(self):
                    value = use_update.pop(remaining_key)
                    setattr(self, remaining_key, value)
        else:
            raise ValueError(
                "Can't use sqlmodel_update() with something that "
                f"is not a dict or SQLModel or Pydantic model: {obj}"
            )
        return self

    # -----------------------------
    # Protobuf Message API methods
    # -----------------------------
    def _to_struct(self) -> _pb_struct_pb2.Struct:
        """Return a google.protobuf.Struct built from this model's data."""
        data = self.model_dump(mode="python")
        s = _pb_struct_pb2.Struct()
        # Struct.update accepts a mapping of JSON-compatible values
        try:
            s.update(data)  # type: ignore[arg-type]
        except Exception:
            # Fallback: go through json_format to coerce non-JSON natives
            s = _pb_json_format.ParseDict(data, _pb_struct_pb2.Struct())
        return s

    def _update_from_struct(self, s: _pb_struct_pb2.Struct) -> None:
        """Merge values from a google.protobuf.Struct into this model."""
        try:
            data = _pb_json_format.MessageToDict(s, preserving_proto_field_name=True)
        except Exception as exc:  # pragma: no cover - defensive
            raise _pb_message_mod.DecodeError(str(exc))
        # Merge dict data into this model
        for key, value in data.items():
            if key in get_model_fields(self):
                setattr(self, key, value)

    def _is_optional_field(self, field_name: str) -> bool:
        try:
            raw_ann = self.__class__.__annotations__.get(field_name, None)
        except Exception:
            raw_ann = None
        if raw_ann is None:
            return False
        origin = get_origin(raw_ann)
        if origin is Union:
            args = getattr(raw_ann, "__args__", ())
            return type(None) in args  # noqa: E721
        return False

    def _is_repeated_field(self, field_name: str) -> bool:
        try:
            raw_ann = self.__class__.__annotations__.get(field_name, None)
        except Exception:
            raw_ann = None
        origin = get_origin(raw_ann)
        if origin is None:
            return False
        try:
            from collections.abc import Sequence as _ABCSequence, Mapping as _ABCMapping
            # Repeated (list-like) and map fields (mapping-like) should be treated as invalid for HasField
            if origin in (list, tuple, set, dict):
                return True
            if isinstance(origin, type) and (issubclass(origin, _ABCSequence) or issubclass(origin, _ABCMapping)):
                return True
        except Exception:
            # Be conservative: if we cannot determine, consider not repeated
            return False
        return False

    def _default_for_field(self, field_name: str) -> Any:
        # Proto3 scalar defaults
        # If field is optional, prefer None to represent absence
        if self._is_optional_field(field_name):
            return None
        try:
            raw_ann = self.__class__.__annotations__.get(field_name, None)
        except Exception:
            raw_ann = None
        typ = raw_ann
        origin = get_origin(typ)
        if origin is Union:
            # Optional handled above; take first non-None
            args = [t for t in getattr(typ, "__args__", ()) if t is not type(None)]  # noqa: E721
            typ = args[0] if args else None
        if typ in (int,):
            return 0
        if typ in (float,):
            return 0.0
        if typ in (bool,):
            return False
        if typ in (str,):
            return ""
        if typ in (bytes, bytearray):
            return b""
        # For sequences/maps, default empty; for messages, None
        try:
            from collections.abc import Sequence as _ABCSequence, Mapping as _ABCMapping
            if origin in (list, set, tuple, dict):
                try:
                    return origin()  # type: ignore[call-arg]
                except Exception:
                    return None
            if isinstance(origin, type) and (issubclass(origin, _ABCSequence) or issubclass(origin, _ABCMapping)):
                # Choose a sensible empty default
                if issubclass(origin, _ABCMapping):
                    return {}
                return []
        except Exception:
            pass
        return None

    def serialize_to_string(self, **kwargs: Any) -> bytes:  # type: ignore[override]
        """Serialize the message to a binary string.

        Raises EncodeError if the message isn't initialized.
        """
        try:
            deterministic = bool(kwargs.get("deterministic", False))
            s = self._to_struct()
            # Struct serialization is stable when deterministic is requested
            # json_format is not needed; protobuf binary wire:
            return s.SerializeToString(deterministic=deterministic)
        except Exception as exc:
            raise _pb_message_mod.EncodeError(str(exc))

    def SerializeToString(self, **kwargs: Any) -> bytes:  # type: ignore[override]
        return self.serialize_to_string(**kwargs)

    def serialize_partial_to_string(self, **kwargs: Any) -> bytes:  # type: ignore[override]
        """Serialize the partial message to a binary string without initialization checks."""
        # Same behavior; SQLModel does not track required fields in protobuf sense
        return self.serialize_to_string(**kwargs)

    def SerializePartialToString(self, **kwargs: Any) -> bytes:  # type: ignore[override]
        return self.serialize_partial_to_string(**kwargs)

    def parse_from_string(self, serialized: bytes) -> None:  # type: ignore[override]
        """Parse serialized protocol buffer data into this message (clears first).

        Raises DecodeError if the input cannot be parsed.
        """
        # Clear first per interface
        self.clear()
        read = self.merge_from_string(serialized)
        # MergeFromString returns bytes read; here we just ignore and return None
        _ = read

    def ParseFromString(self, serialized: bytes) -> None:  # type: ignore[override]
        return self.parse_from_string(serialized)

    def merge_from_string(self, serialized: bytes) -> int:  # type: ignore[override]
        """Merge serialized protocol buffer data into this message and return bytes read.

        Raises DecodeError if the input cannot be parsed.
        """
        try:
            s = _pb_struct_pb2.Struct()
            # For non-group messages this should consume all bytes
            read = s.MergeFromString(serialized)
            self._update_from_struct(s)
            return read
        except Exception as exc:
            raise _pb_message_mod.DecodeError(str(exc))

    def MergeFromString(self, serialized: bytes) -> int:  # type: ignore[override]
        return self.merge_from_string(serialized)

    def merge_from(self, other_msg: Message) -> None:  # type: ignore[override]
        """Merge the contents of another message into this one."""
        if isinstance(other_msg, SQLModel):
            for key in get_model_fields(other_msg):
                setattr(self, key, getattr(other_msg, key))
            return
        # Fallback: try to convert any Message to dict via json_format, then merge
        try:
            data = _pb_json_format.MessageToDict(other_msg, preserving_proto_field_name=True)
            for key, value in data.items():
                if key in get_model_fields(self):
                    setattr(self, key, value)
        except Exception as exc:
            raise _pb_message_mod.DecodeError(str(exc))

    def MergeFrom(self, other_msg: Message) -> None:  # type: ignore[override]
        return self.merge_from(other_msg)

    def copy_from(self, other_msg: Message) -> None:  # type: ignore[override]
        """Clear this message and then merge from the given message."""
        self.clear()
        self.merge_from(other_msg)

    def CopyFrom(self, other_msg: Message) -> None:  # type: ignore[override]
        return self.copy_from(other_msg)

    def clear(self) -> None:  # type: ignore[override]
        """Clear all fields in the message to their default values."""
        for key in list(get_model_fields(self).keys()):
            try:
                setattr(self, key, self._default_for_field(key))
            except Exception:
                pass

    def Clear(self) -> None:  # type: ignore[override]
        return self.clear()

    def clear_field(self, field_name: str) -> None:  # type: ignore[override]
        """Clear the contents of the given field.

        Raises ValueError if the field name is not a member.
        """
        if field_name not in get_model_fields(self):
            raise ValueError(f"Field {field_name!r} is not a member of this message.")
        setattr(self, field_name, self._default_for_field(field_name))

    def ClearField(self, field_name: str) -> None:  # type: ignore[override]
        return self.clear_field(field_name)

    def has_field(self, field_name: str) -> bool:  # type: ignore[override]
        """Check if a field is set (presence).

        In proto3, valid only for optional scalars and sub-messages; raises for
        repeated fields and non-optional scalars.
        """
        if field_name not in get_model_fields(self):
            raise ValueError(f"Field {field_name!r} is not a member of this message.")
        # In proto3, HasField is only valid for sub-messages, oneofs, and optional scalars
        if self._is_repeated_field(field_name):
            raise ValueError("HasField() is not valid for repeated fields in proto3")
        if not self._is_optional_field(field_name):
            # Treat BaseModel (message-like) as allowing presence
            value = getattr(self, field_name, None)
            if isinstance(value, BaseModel):
                return value is not None
            raise ValueError("HasField() is not valid for non-optional scalar fields in proto3")
        return getattr(self, field_name, None) is not None

    def HasField(self, field_name: str) -> bool:  # type: ignore[override]
        return self.has_field(field_name)

    def list_fields(self) -> List[Tuple[Any, Any]]:  # type: ignore[override]
        """Return a list of (FieldDescriptor, value) for present fields.

        This dynamic implementation does not expose FieldDescriptors; returns [].
        """
        # We do not have real FieldDescriptors; return empty list for compatibility
        present: List[Tuple[Any, Any]] = []
        return present

    def ListFields(self) -> List[Tuple[Any, Any]]:  # type: ignore[override]
        return self.list_fields()

    def is_initialized(self) -> bool:  # type: ignore[override]
        """Return True if the message is initialized (proto3: always True)."""
        # Proto3 has no required fields; always initialized
        return True

    def IsInitialized(self) -> bool:  # type: ignore[override]
        return self.is_initialized()

    def byte_size(self) -> int:  # type: ignore[override]
        """Return the number of bytes required to serialize this message."""
        try:
            return len(self.serialize_to_string())
        except _pb_message_mod.EncodeError:
            return 0

    def ByteSize(self) -> int:  # type: ignore[override]
        return self.byte_size()

    def discard_unknown_fields(self) -> None:  # type: ignore[override]
        """Clear all fields in the UnknownFieldSet (no-op for dynamic model)."""
        # No unknown fields are tracked when using Struct
        return None

    def DiscardUnknownFields(self) -> None:  # type: ignore[override]
        return self.discard_unknown_fields()

    @staticmethod
    def register_extension(extension_handle: Any) -> None:  # type: ignore[override]
        """Register an extension (not supported for this dynamic message)."""
        # Not supported for dynamic SQLModel-based messages
        return None

    @staticmethod
    def RegisterExtension(extension_handle: Any) -> None:  # type: ignore[override]
        return SQLModel.register_extension(extension_handle)

    def unknown_fields(self) -> Any:  # type: ignore[override]
        """Return the UnknownFieldSet (empty for this dynamic message)."""
        # Not tracking unknown fields; return empty Struct for API compatibility
        return _pb_struct_pb2.Struct()

    def UnknownFields(self) -> Any:  # type: ignore[override]
        return self.unknown_fields()

    def set_in_parent(self) -> None:  # type: ignore[override]
        """Mark this as present in the parent (no-op)."""
        # No-op: presence is implicit in SQLModel
        return None

    def SetInParent(self) -> None:  # type: ignore[override]
        return self.set_in_parent()

    def which_oneof(self, oneof_group: str) -> Optional[str]:  # type: ignore[override]
        """Return the name of the field set inside a oneof group, or None.

        This dynamic model does not define oneof groups; always returns None.
        """
        # SQLModel does not model oneof groups
        return None

    def WhichOneof(self, oneof_group: str) -> Optional[str]:  # type: ignore[override]
        return self.which_oneof(oneof_group)
