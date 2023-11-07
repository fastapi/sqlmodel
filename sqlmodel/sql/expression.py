# WARNING: do not modify this code, it is generated by expression.py.jinja2

from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Mapping,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.sql.expression import Select as _Select

_TSelect = TypeVar("_TSelect")


class Select(_Select[Tuple[_TSelect]]):
    inherit_cache = True


# This is not comparable to sqlalchemy.sql.selectable.ScalarSelect, that has a different
# purpose. This is the same as a normal SQLAlchemy Select class where there's only one
# entity, so the result will be converted to a scalar by default. This way writing
# for loops on the results will feel natural.
class SelectOfScalar(_Select[Tuple[_TSelect]]):
    inherit_cache = True


if TYPE_CHECKING:  # pragma: no cover
    from ..main import SQLModel

# Generated TypeVars start


_TScalar_0 = TypeVar(
    "_TScalar_0",
    Column,  # type: ignore
    Sequence,  # type: ignore
    Mapping,  # type: ignore
    UUID,
    datetime,
    float,
    int,
    bool,
    bytes,
    str,
    None,
)

_TModel_0 = TypeVar("_TModel_0", bound="SQLModel")


_TScalar_1 = TypeVar(
    "_TScalar_1",
    Column,  # type: ignore
    Sequence,  # type: ignore
    Mapping,  # type: ignore
    UUID,
    datetime,
    float,
    int,
    bool,
    bytes,
    str,
    None,
)

_TModel_1 = TypeVar("_TModel_1", bound="SQLModel")


_TScalar_2 = TypeVar(
    "_TScalar_2",
    Column,  # type: ignore
    Sequence,  # type: ignore
    Mapping,  # type: ignore
    UUID,
    datetime,
    float,
    int,
    bool,
    bytes,
    str,
    None,
)

_TModel_2 = TypeVar("_TModel_2", bound="SQLModel")


_TScalar_3 = TypeVar(
    "_TScalar_3",
    Column,  # type: ignore
    Sequence,  # type: ignore
    Mapping,  # type: ignore
    UUID,
    datetime,
    float,
    int,
    bool,
    bytes,
    str,
    None,
)

_TModel_3 = TypeVar("_TModel_3", bound="SQLModel")


# Generated TypeVars end


@overload
def select(entity_0: _TScalar_0) -> SelectOfScalar[_TScalar_0]:  # type: ignore
    ...


@overload
def select(entity_0: Type[_TModel_0]) -> SelectOfScalar[_TModel_0]:  # type: ignore
    ...


# Generated overloads start


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
) -> Select[Tuple[_TScalar_0, _TScalar_1]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
) -> Select[Tuple[_TScalar_0, _TModel_1]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
) -> Select[Tuple[_TModel_0, _TScalar_1]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
) -> Select[Tuple[_TModel_0, _TModel_1]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TModel_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
) -> Select[Tuple[_TScalar_0, _TModel_1, _TScalar_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
) -> Select[Tuple[_TScalar_0, _TModel_1, _TModel_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
) -> Select[Tuple[_TModel_0, _TScalar_1, _TScalar_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
) -> Select[Tuple[_TModel_0, _TScalar_1, _TModel_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
) -> Select[Tuple[_TModel_0, _TModel_1, _TScalar_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
) -> Select[Tuple[_TModel_0, _TModel_1, _TModel_2]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TModel_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TModel_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TModel_1, _TScalar_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TScalar_0, _TModel_1, _TScalar_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TModel_1, _TModel_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TScalar_0, _TModel_1, _TModel_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TModel_0, _TScalar_1, _TScalar_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TModel_0, _TScalar_1, _TScalar_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TModel_0, _TScalar_1, _TModel_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: _TScalar_1,
    entity_2: Type[_TModel_2],
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TModel_0, _TScalar_1, _TModel_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TModel_0, _TModel_1, _TScalar_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: _TScalar_2,
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TModel_0, _TModel_1, _TScalar_2, _TModel_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TModel_0, _TModel_1, _TModel_2, _TScalar_3]]:
    ...


@overload
def select(  # type: ignore
    entity_0: Type[_TModel_0],
    entity_1: Type[_TModel_1],
    entity_2: Type[_TModel_2],
    entity_3: Type[_TModel_3],
) -> Select[Tuple[_TModel_0, _TModel_1, _TModel_2, _TModel_3]]:
    ...


# Generated overloads end


def select(*entities: Any) -> Union[Select, SelectOfScalar]:  # type: ignore
    if len(entities) == 1:
        return SelectOfScalar(*entities)  # type: ignore
    return Select(*entities)  # type: ignore


# TODO: add several @overload from Python types to SQLAlchemy equivalents
def col(column_expression: Any) -> ColumnClause:  # type: ignore
    if not isinstance(column_expression, (ColumnClause, Column, InstrumentedAttribute)):
        raise RuntimeError(f"Not a SQLAlchemy column: {column_expression}")
    return column_expression  # type: ignore
