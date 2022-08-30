import ipaddress
import uuid
import weakref
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import (
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
)

from pydantic import BaseConfig, BaseModel
from pydantic.errors import ConfigError, DictError
from pydantic.fields import SHAPE_SINGLETON
from pydantic.fields import FieldInfo as PydanticFieldInfo
from pydantic.fields import ModelField, Undefined, UndefinedType
from pydantic.main import ModelMetaclass, validate_model
from pydantic.typing import ForwardRef, NoArgAnyCallable, resolve_annotations
from pydantic.utils import ROOT_KEY, Representation
from sqlalchemy import Boolean, Column, Date, DateTime
from sqlalchemy import Enum as sa_Enum
from sqlalchemy import Float, ForeignKey, Integer, Interval, Numeric, inspect
from sqlalchemy.orm import RelationshipProperty, declared_attr, registry, relationship
from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.instrumentation import is_instrumented
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import LargeBinary, Time

from .sql.sqltypes import GUID, AutoString

_T = TypeVar("_T")


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    return lambda a: a


class FieldInfo(PydanticFieldInfo):
    def __init__(self, default: Any = Undefined, **kwargs: Any) -> None:
        primary_key = kwargs.pop("primary_key", False)
        nullable = kwargs.pop("nullable", Undefined)
        foreign_key = kwargs.pop("foreign_key", Undefined)
        unique = kwargs.pop("unique", False)
        index = kwargs.pop("index", Undefined)
        sa_column = kwargs.pop("sa_column", Undefined)
        sa_column_args = kwargs.pop("sa_column_args", Undefined)
        sa_column_kwargs = kwargs.pop("sa_column_kwargs", Undefined)
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
        super().__init__(default=default, **kwargs)
        self.primary_key = primary_key
        self.nullable = nullable
        self.foreign_key = foreign_key
        self.unique = unique
        self.index = index
        self.sa_column = sa_column
        self.sa_column_args = sa_column_args
        self.sa_column_kwargs = sa_column_kwargs


class RelationshipInfo(Representation):
    def __init__(
        self,
        *,
        back_populates: Optional[str] = None,
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
        self.link_model = link_model
        self.sa_relationship = sa_relationship
        self.sa_relationship_args = sa_relationship_args
        self.sa_relationship_kwargs = sa_relationship_kwargs


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
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    primary_key: bool = False,
    foreign_key: Optional[Any] = None,
    unique: bool = False,
    nullable: Union[bool, UndefinedType] = Undefined,
    index: Union[bool, UndefinedType] = Undefined,
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
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_items=min_items,
        max_items=max_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        primary_key=primary_key,
        foreign_key=foreign_key,
        unique=unique,
        nullable=nullable,
        index=index,
        sa_column=sa_column,
        sa_column_args=sa_column_args,
        sa_column_kwargs=sa_column_kwargs,
        **current_schema_extra,
    )
    field_info._validate()
    return field_info


def Relationship(
    *,
    back_populates: Optional[str] = None,
    link_model: Optional[Any] = None,
    sa_relationship: Optional[RelationshipProperty] = None,  # type: ignore
    sa_relationship_args: Optional[Sequence[Any]] = None,
    sa_relationship_kwargs: Optional[Mapping[str, Any]] = None,
) -> Any:
    relationship_info = RelationshipInfo(
        back_populates=back_populates,
        link_model=link_model,
        sa_relationship=sa_relationship,
        sa_relationship_args=sa_relationship_args,
        sa_relationship_kwargs=sa_relationship_kwargs,
    )
    return relationship_info


@__dataclass_transform__(kw_only_default=True, field_descriptors=(Field, FieldInfo))
class SQLModelMetaclass(ModelMetaclass, DeclarativeMeta):
    __sqlmodel_relationships__: Dict[str, RelationshipInfo]
    __config__: Type[BaseConfig]
    __fields__: Dict[str, ModelField]

    # Replicate SQLAlchemy
    def __setattr__(cls, name: str, value: Any) -> None:
        if getattr(cls.__config__, "table", False):
            DeclarativeMeta.__setattr__(cls, name, value)
        else:
            super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        if getattr(cls.__config__, "table", False):
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
        original_annotations = resolve_annotations(
            class_dict.get("__annotations__", {}), class_dict.get("__module__", None)
        )
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
        pydantic_kwargs = kwargs.copy()
        config_kwargs = {
            key: pydantic_kwargs.pop(key)
            for key in pydantic_kwargs.keys() & allowed_config_kwargs
        }
        new_cls = super().__new__(cls, name, bases, dict_used, **config_kwargs)
        new_cls.__annotations__ = {
            **relationship_annotations,
            **pydantic_annotations,
            **new_cls.__annotations__,
        }

        def get_config(name: str) -> Any:
            config_class_value = getattr(new_cls.__config__, name, Undefined)
            if config_class_value is not Undefined:
                return config_class_value
            kwarg_value = kwargs.get(name, Undefined)
            if kwarg_value is not Undefined:
                return kwarg_value
            return Undefined

        config_table = get_config("table")
        if config_table is True:
            # If it was passed by kwargs, ensure it's also set in config
            new_cls.__config__.table = config_table
            for k, v in new_cls.__fields__.items():
                col = get_column_from_field(v)
                setattr(new_cls, k, col)
            # Set a config flag to tell FastAPI that this should be read with a field
            # in orm_mode instead of preemptively converting it to a dict.
            # This could be done by reading new_cls.__config__.table in FastAPI, but
            # that's very specific about SQLModel, so let's have another config that
            # other future tools based on Pydantic can use.
            new_cls.__config__.read_with_orm_mode = True

        config_registry = get_config("registry")
        if config_registry is not Undefined:
            config_registry = cast(registry, config_registry)
            # If it was passed by kwargs, ensure it's also set in config
            new_cls.__config__.registry = config_table
            setattr(new_cls, "_sa_registry", config_registry)
            setattr(new_cls, "metadata", config_registry.metadata)
            setattr(new_cls, "__abstract__", True)
        return new_cls

    # Override SQLAlchemy, allow both SQLAlchemy and plain Pydantic models
    def __init__(
        cls, classname: str, bases: Tuple[type, ...], dict_: Dict[str, Any], **kw: Any
    ) -> None:
        # Only one of the base classes (or the current one) should be a table model
        # this allows FastAPI cloning a SQLModel for the response_model without
        # trying to create a new SQLAlchemy, for a new table, with the same name, that
        # triggers an error
        base_is_table = False
        for base in bases:
            config = getattr(base, "__config__")
            if config and getattr(config, "table", False):
                base_is_table = True
                break
        if getattr(cls.__config__, "table", False) and not base_is_table:
            dict_used = dict_.copy()
            for field_name, field_value in cls.__fields__.items():
                dict_used[field_name] = get_column_from_field(field_value)
            for rel_name, rel_info in cls.__sqlmodel_relationships__.items():
                if rel_info.sa_relationship:
                    # There's a SQLAlchemy relationship declared, that takes precedence
                    # over anything else, use that and continue with the next attribute
                    dict_used[rel_name] = rel_info.sa_relationship
                    continue
                ann = cls.__annotations__[rel_name]
                temp_field = ModelField.infer(
                    name=rel_name,
                    value=rel_info,
                    annotation=ann,
                    class_validators=None,
                    config=BaseConfig,
                )
                relationship_to = temp_field.type_
                if isinstance(temp_field.type_, ForwardRef):
                    relationship_to = temp_field.type_.__forward_arg__
                rel_kwargs: Dict[str, Any] = {}
                if rel_info.back_populates:
                    rel_kwargs["back_populates"] = rel_info.back_populates
                if rel_info.link_model:
                    ins = inspect(rel_info.link_model)
                    local_table = getattr(ins, "local_table")
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
                rel_value: RelationshipProperty = relationship(  # type: ignore
                    relationship_to, *rel_args, **rel_kwargs
                )
                dict_used[rel_name] = rel_value
                setattr(cls, rel_name, rel_value)  # Fix #315
            DeclarativeMeta.__init__(cls, classname, bases, dict_used, **kw)
        else:
            ModelMetaclass.__init__(cls, classname, bases, dict_, **kw)


def get_sqlachemy_type(field: ModelField) -> Any:
    if issubclass(field.type_, str):
        if field.field_info.max_length:
            return AutoString(length=field.field_info.max_length)
        return AutoString
    if issubclass(field.type_, float):
        return Float
    if issubclass(field.type_, bool):
        return Boolean
    if issubclass(field.type_, int):
        return Integer
    if issubclass(field.type_, datetime):
        return DateTime
    if issubclass(field.type_, date):
        return Date
    if issubclass(field.type_, timedelta):
        return Interval
    if issubclass(field.type_, time):
        return Time
    if issubclass(field.type_, Enum):
        return sa_Enum(field.type_)
    if issubclass(field.type_, bytes):
        return LargeBinary
    if issubclass(field.type_, Decimal):
        return Numeric(
            precision=getattr(field.type_, "max_digits", None),
            scale=getattr(field.type_, "decimal_places", None),
        )
    if issubclass(field.type_, ipaddress.IPv4Address):
        return AutoString
    if issubclass(field.type_, ipaddress.IPv4Network):
        return AutoString
    if issubclass(field.type_, ipaddress.IPv6Address):
        return AutoString
    if issubclass(field.type_, ipaddress.IPv6Network):
        return AutoString
    if issubclass(field.type_, Path):
        return AutoString
    if issubclass(field.type_, uuid.UUID):
        return GUID
    raise ValueError(f"The field {field.name} has no matching SQLAlchemy type")


def get_column_from_field(field: ModelField) -> Column:  # type: ignore
    sa_column = getattr(field.field_info, "sa_column", Undefined)
    if isinstance(sa_column, Column):
        return sa_column
    sa_type = get_sqlachemy_type(field)
    primary_key = getattr(field.field_info, "primary_key", False)
    index = getattr(field.field_info, "index", Undefined)
    if index is Undefined:
        index = False
    nullable = not primary_key and _is_field_noneable(field)
    # Override derived nullability if the nullable property is set explicitly
    # on the field
    if hasattr(field.field_info, "nullable"):
        field_nullable = getattr(field.field_info, "nullable")
        if field_nullable != Undefined:
            nullable = field_nullable
    args = []
    foreign_key = getattr(field.field_info, "foreign_key", None)
    unique = getattr(field.field_info, "unique", False)
    if foreign_key:
        args.append(ForeignKey(foreign_key))
    kwargs = {
        "primary_key": primary_key,
        "nullable": nullable,
        "index": index,
        "unique": unique,
    }
    sa_default = Undefined
    if field.field_info.default_factory:
        sa_default = field.field_info.default_factory
    elif field.field_info.default is not Undefined:
        sa_default = field.field_info.default
    if sa_default is not Undefined:
        kwargs["default"] = sa_default
    sa_column_args = getattr(field.field_info, "sa_column_args", Undefined)
    if sa_column_args is not Undefined:
        args.extend(list(cast(Sequence[Any], sa_column_args)))
    sa_column_kwargs = getattr(field.field_info, "sa_column_kwargs", Undefined)
    if sa_column_kwargs is not Undefined:
        kwargs.update(cast(Dict[Any, Any], sa_column_kwargs))
    return Column(sa_type, *args, **kwargs)  # type: ignore


class_registry = weakref.WeakValueDictionary()  # type: ignore

default_registry = registry()


def _value_items_is_true(v: Any) -> bool:
    # Re-implement Pydantic's ValueItems.is_true() as it hasn't been released as of
    # the current latest, Pydantic 1.8.2
    return v is True or v is ...


_TSQLModel = TypeVar("_TSQLModel", bound="SQLModel")


class SQLModel(BaseModel, metaclass=SQLModelMetaclass, registry=default_registry):
    # SQLAlchemy needs to set weakref(s), Pydantic will set the other slots values
    __slots__ = ("__weakref__",)
    __tablename__: ClassVar[Union[str, Callable[..., str]]]
    __sqlmodel_relationships__: ClassVar[Dict[str, RelationshipProperty]]  # type: ignore
    __name__: ClassVar[str]
    metadata: ClassVar[MetaData]

    class Config:
        orm_mode = True

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        new_object = super().__new__(cls)
        # SQLAlchemy doesn't call __init__ on the base class
        # Ref: https://docs.sqlalchemy.org/en/14/orm/constructors.html
        # Set __fields_set__ here, that would have been set when calling __init__
        # in the Pydantic model so that when SQLAlchemy sets attributes that are
        # added (e.g. when querying from DB) to the __fields_set__, this already exists
        object.__setattr__(new_object, "__fields_set__", set())
        return new_object

    def __init__(__pydantic_self__, **data: Any) -> None:
        # Uses something other than `self` the first arg to allow "self" as a
        # settable attribute
        values, fields_set, validation_error = validate_model(
            __pydantic_self__.__class__, data
        )
        # Only raise errors if not a SQLModel model
        if (
            not getattr(__pydantic_self__.__config__, "table", False)
            and validation_error
        ):
            raise validation_error
        # Do not set values as in Pydantic, pass them through setattr, so SQLAlchemy
        # can handle them
        # object.__setattr__(__pydantic_self__, '__dict__', values)
        for key, value in values.items():
            setattr(__pydantic_self__, key, value)
        object.__setattr__(__pydantic_self__, "__fields_set__", fields_set)
        non_pydantic_keys = data.keys() - values.keys()
        for key in non_pydantic_keys:
            if key in __pydantic_self__.__sqlmodel_relationships__:
                setattr(__pydantic_self__, key, data[key])

    def __setattr__(self, name: str, value: Any) -> None:
        if name in {"_sa_instance_state"}:
            self.__dict__[name] = value
            return
        else:
            # Set in SQLAlchemy, before Pydantic to trigger events and updates
            if getattr(self.__config__, "table", False) and is_instrumented(self, name):
                set_attribute(self, name, value)
            # Set in Pydantic model to trigger possible validation changes, only for
            # non relationship values
            if name not in self.__sqlmodel_relationships__:
                super().__setattr__(name, value)

    @classmethod
    def from_orm(
        cls: Type[_TSQLModel], obj: Any, update: Optional[Dict[str, Any]] = None
    ) -> _TSQLModel:
        # Duplicated from Pydantic
        if not cls.__config__.orm_mode:
            raise ConfigError(
                "You must have the config attribute orm_mode=True to use from_orm"
            )
        obj = {ROOT_KEY: obj} if cls.__custom_root_type__ else cls._decompose_class(obj)
        # SQLModel, support update dict
        if update is not None:
            obj = {**obj, **update}
        # End SQLModel support dict
        if not getattr(cls.__config__, "table", False):
            # If not table, normal Pydantic code
            m: _TSQLModel = cls.__new__(cls)
        else:
            # If table, create the new instance normally to make SQLAlchemy create
            # the _sa_instance_state attribute
            m = cls()
        values, fields_set, validation_error = validate_model(cls, obj)
        if validation_error:
            raise validation_error
        # Updated to trigger SQLAlchemy internal handling
        if not getattr(cls.__config__, "table", False):
            object.__setattr__(m, "__dict__", values)
        else:
            for key, value in values.items():
                setattr(m, key, value)
        # Continue with standard Pydantic logic
        object.__setattr__(m, "__fields_set__", fields_set)
        m._init_private_attributes()
        return m

    @classmethod
    def parse_obj(
        cls: Type[_TSQLModel], obj: Any, update: Optional[Dict[str, Any]] = None
    ) -> _TSQLModel:
        obj = cls._enforce_dict_if_root(obj)
        # SQLModel, support update dict
        if update is not None:
            obj = {**obj, **update}
        # End SQLModel support dict
        return super().parse_obj(obj)

    def __repr_args__(self) -> Sequence[Tuple[Optional[str], Any]]:
        # Don't show SQLAlchemy private attributes
        return [(k, v) for k, v in self.__dict__.items() if not k.startswith("_sa_")]

    # From Pydantic, override to enforce validation with dict
    @classmethod
    def validate(cls: Type[_TSQLModel], value: Any) -> _TSQLModel:
        if isinstance(value, cls):
            return value.copy() if cls.__config__.copy_on_model_validation else value

        value = cls._enforce_dict_if_root(value)
        if isinstance(value, dict):
            values, fields_set, validation_error = validate_model(cls, value)
            if validation_error:
                raise validation_error
            model = cls(**value)
            # Reset fields set, this would have been done in Pydantic in __init__
            object.__setattr__(model, "__fields_set__", fields_set)
            return model
        elif cls.__config__.orm_mode:
            return cls.from_orm(value)
        elif cls.__custom_root_type__:
            return cls.parse_obj(value)
        else:
            try:
                value_as_dict = dict(value)
            except (TypeError, ValueError) as e:
                raise DictError() from e
            return cls(**value_as_dict)

    # From Pydantic, override to only show keys from fields, omit SQLAlchemy attributes
    def _calculate_keys(
        self,
        include: Optional[Mapping[Union[int, str], Any]],
        exclude: Optional[Mapping[Union[int, str], Any]],
        exclude_unset: bool,
        update: Optional[Dict[str, Any]] = None,
    ) -> Optional[AbstractSet[str]]:
        if include is None and exclude is None and not exclude_unset:
            # Original in Pydantic:
            # return None
            # Updated to not return SQLAlchemy attributes
            # Do not include relationships as that would easily lead to infinite
            # recursion, or traversing the whole database
            return self.__fields__.keys()  # | self.__sqlmodel_relationships__.keys()

        keys: AbstractSet[str]
        if exclude_unset:
            keys = self.__fields_set__.copy()
        else:
            # Original in Pydantic:
            # keys = self.__dict__.keys()
            # Updated to not return SQLAlchemy attributes
            # Do not include relationships as that would easily lead to infinite
            # recursion, or traversing the whole database
            keys = self.__fields__.keys()  # | self.__sqlmodel_relationships__.keys()
        if include is not None:
            keys &= include.keys()

        if update:
            keys -= update.keys()

        if exclude:
            keys -= {k for k, v in exclude.items() if _value_items_is_true(v)}

        return keys

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def _is_field_noneable(field: ModelField) -> bool:
    if not field.required:
        # Taken from [Pydantic](https://github.com/samuelcolvin/pydantic/blob/v1.8.2/pydantic/fields.py#L946-L947)
        return field.allow_none and (
            field.shape != SHAPE_SINGLETON or not field.sub_fields
        )
    return False
