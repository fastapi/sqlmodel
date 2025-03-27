# WARNING: do not modify this code, it is generated by _expression_select_gen.py.jinja2

from datetime import datetime
from typing import (
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

from sqlalchemy import (
    Column,
)
from sqlalchemy.sql.elements import (
    SQLCoreOperations,
)
from sqlalchemy.sql.roles import TypedColumnsClauseRole

from ._expression_select_cls import Select, SelectOfScalar

_T = TypeVar("_T")


_TCCA = Union[
    TypedColumnsClauseRole[_T],
    SQLCoreOperations[_T],
    Type[_T],
]

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

_T0 = TypeVar("_T0")


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

_T1 = TypeVar("_T1")


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

_T2 = TypeVar("_T2")


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

_T3 = TypeVar("_T3")


_TScalar_4 = TypeVar(
    "_TScalar_4",
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

_T4 = TypeVar("_T4")


# Generated TypeVars end


@overload
def select(__ent0: _TCCA[_T0]) -> SelectOfScalar[_T0]: ...


@overload
def select(__ent0: _TScalar_0) -> SelectOfScalar[_TScalar_0]:  # type: ignore
    ...


# Generated overloads start


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
) -> Select[Tuple[_T0, _T1]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
) -> Select[Tuple[_T0, _TScalar_1]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
) -> Select[Tuple[_TScalar_0, _T1]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
) -> Select[Tuple[_TScalar_0, _TScalar_1]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
) -> Select[Tuple[_T0, _T1, _T2]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
) -> Select[Tuple[_T0, _T1, _TScalar_2]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
) -> Select[Tuple[_T0, _TScalar_1, _T2]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
) -> Select[Tuple[_TScalar_0, _T1, _T2]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_T0, _T1, _T2, _T3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_T0, _T1, _T2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_T0, _T1, _TScalar_2, _T3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_T0, _T1, _TScalar_2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_T0, _TScalar_1, _T2, _T3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_T0, _TScalar_1, _T2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _T3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_TScalar_0, _T1, _T2, _T3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _T1, _T2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _T3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _T3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _T3]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _TScalar_3]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _T1, _T2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _T1, _T2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _T1, _T2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _T1, _T2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _T1, _TScalar_2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _T1, _TScalar_2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _T1, _TScalar_2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _T1, _TScalar_2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _TScalar_1, _T2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _TScalar_1, _T2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _TScalar_1, _T2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _TScalar_1, _T2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    __ent0: _TCCA[_T0],
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_T0, _TScalar_1, _TScalar_2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _T1, _T2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _T1, _T2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _T1, _T2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _T1, _T2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    __ent1: _TCCA[_T1],
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _T1, _TScalar_2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    __ent2: _TCCA[_T2],
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _T2, _TScalar_3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _T3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    __ent3: _TCCA[_T3],
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _T3, _TScalar_4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    __ent4: _TCCA[_T4],
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _TScalar_3, _T4]]: ...


@overload
def select(  # type: ignore
    entity_0: _TScalar_0,
    entity_1: _TScalar_1,
    entity_2: _TScalar_2,
    entity_3: _TScalar_3,
    entity_4: _TScalar_4,
) -> Select[Tuple[_TScalar_0, _TScalar_1, _TScalar_2, _TScalar_3, _TScalar_4]]: ...


# Generated overloads end


def select(*entities: Any) -> Union[Select, SelectOfScalar]:  # type: ignore
    if len(entities) == 1:
        return SelectOfScalar(*entities)
    return Select(*entities)
