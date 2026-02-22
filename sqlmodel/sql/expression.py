from collections.abc import Iterable, Mapping, Sequence
from typing import (
    Any,
    Literal,
    Optional,
    TypeVar,
)

import sqlalchemy
from sqlalchemy import (
    Column,
    ColumnElement,
    Extract,
    FunctionElement,
    FunctionFilter,
    Label,
    Over,
    TypeCoerce,
    WithinGroup,
)
from sqlalchemy.orm import InstrumentedAttribute, Mapped
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
    _ColumnExpressionOrLiteralArgument,
    _ColumnExpressionOrStrLabelArgument,
)
from sqlalchemy.sql.elements import (
    BinaryExpression,
    Case,
    Cast,
    CollectionAggregate,
    ColumnClause,
    TryCast,
    UnaryExpression,
)
from sqlalchemy.sql.type_api import TypeEngine

from ._expression_select_cls import Select as Select
from ._expression_select_cls import SelectOfScalar as SelectOfScalar
from ._expression_select_gen import select as select

_T = TypeVar("_T")

_TypeEngineArgument = type[TypeEngine[_T]] | TypeEngine[_T]

# Redefine operators that would only take a column expression to also take the (virtual)
# types of Pydantic models, e.g. str instead of only Mapped[str].


def all_(expr: _ColumnExpressionArgument[_T] | _T) -> CollectionAggregate[bool]:
    return sqlalchemy.all_(expr)  # type: ignore[arg-type]


def and_(
    initial_clause: Literal[True] | _ColumnExpressionArgument[bool] | bool,
    *clauses: _ColumnExpressionArgument[bool] | bool,
) -> ColumnElement[bool]:
    return sqlalchemy.and_(initial_clause, *clauses)  # type: ignore[arg-type]


def any_(expr: _ColumnExpressionArgument[_T] | _T) -> CollectionAggregate[bool]:
    return sqlalchemy.any_(expr)  # type: ignore[arg-type]


def asc(
    column: _ColumnExpressionOrStrLabelArgument[_T] | _T,
) -> UnaryExpression[_T]:
    return sqlalchemy.asc(column)  # type: ignore[arg-type]


def collate(
    expression: _ColumnExpressionArgument[str] | str, collation: str
) -> BinaryExpression[str]:
    return sqlalchemy.collate(expression, collation)  # type: ignore[arg-type]


def between(
    expr: _ColumnExpressionOrLiteralArgument[_T] | _T,
    lower_bound: Any,
    upper_bound: Any,
    symmetric: bool = False,
) -> BinaryExpression[bool]:
    return sqlalchemy.between(expr, lower_bound, upper_bound, symmetric=symmetric)


def not_(clause: _ColumnExpressionArgument[_T] | _T) -> ColumnElement[_T]:
    return sqlalchemy.not_(clause)  # type: ignore[arg-type]


def case(
    *whens: tuple[_ColumnExpressionArgument[bool] | bool, Any] | Mapping[Any, Any],
    value: Any | None = None,
    else_: Any | None = None,
) -> Case[Any]:
    return sqlalchemy.case(*whens, value=value, else_=else_)  # type: ignore[arg-type]


def cast(
    expression: _ColumnExpressionOrLiteralArgument[Any] | Any,
    type_: "_TypeEngineArgument[_T]",
) -> Cast[_T]:
    return sqlalchemy.cast(expression, type_)


def try_cast(
    expression: _ColumnExpressionOrLiteralArgument[Any] | Any,
    type_: "_TypeEngineArgument[_T]",
) -> TryCast[_T]:
    return sqlalchemy.try_cast(expression, type_)


def desc(
    column: _ColumnExpressionOrStrLabelArgument[_T] | _T,
) -> UnaryExpression[_T]:
    return sqlalchemy.desc(column)  # type: ignore[arg-type]


def distinct(expr: _ColumnExpressionArgument[_T] | _T) -> UnaryExpression[_T]:
    return sqlalchemy.distinct(expr)  # type: ignore[arg-type]


def bitwise_not(expr: _ColumnExpressionArgument[_T] | _T) -> UnaryExpression[_T]:
    return sqlalchemy.bitwise_not(expr)  # type: ignore[arg-type]


def extract(field: str, expr: _ColumnExpressionArgument[Any] | Any) -> Extract:
    return sqlalchemy.extract(field, expr)


def funcfilter(
    func: FunctionElement[_T], *criterion: _ColumnExpressionArgument[bool] | bool
) -> FunctionFilter[_T]:
    return sqlalchemy.funcfilter(func, *criterion)  # type: ignore[arg-type]


def label(
    name: str,
    element: _ColumnExpressionArgument[_T] | _T,
    type_: Optional["_TypeEngineArgument[_T]"] = None,
) -> Label[_T]:
    return sqlalchemy.label(name, element, type_=type_)  # type: ignore[arg-type]


def nulls_first(
    column: _ColumnExpressionArgument[_T] | _T,
) -> UnaryExpression[_T]:
    return sqlalchemy.nulls_first(column)  # type: ignore[arg-type]


def nulls_last(column: _ColumnExpressionArgument[_T] | _T) -> UnaryExpression[_T]:
    return sqlalchemy.nulls_last(column)  # type: ignore[arg-type]


def or_(
    initial_clause: Literal[False] | _ColumnExpressionArgument[bool] | bool,
    *clauses: _ColumnExpressionArgument[bool] | bool,
) -> ColumnElement[bool]:
    return sqlalchemy.or_(initial_clause, *clauses)  # type: ignore[arg-type]


def over(
    element: FunctionElement[_T],
    partition_by: Iterable[_ColumnExpressionArgument[Any] | Any]
    | _ColumnExpressionArgument[Any]
    | Any
    | None = None,
    order_by: Iterable[_ColumnExpressionArgument[Any] | Any]
    | _ColumnExpressionArgument[Any]
    | Any
    | None = None,
    range_: tuple[int | None, int | None] | None = None,
    rows: tuple[int | None, int | None] | None = None,
) -> Over[_T]:
    return sqlalchemy.over(
        element, partition_by=partition_by, order_by=order_by, range_=range_, rows=rows
    )


def tuple_(
    *clauses: _ColumnExpressionArgument[Any] | Any,
    types: Sequence["_TypeEngineArgument[Any]"] | None = None,
) -> tuple[Any, ...]:
    return sqlalchemy.tuple_(*clauses, types=types)  # type: ignore[return-value]


def type_coerce(
    expression: _ColumnExpressionOrLiteralArgument[Any] | Any,
    type_: "_TypeEngineArgument[_T]",
) -> TypeCoerce[_T]:
    return sqlalchemy.type_coerce(expression, type_)


def within_group(
    element: FunctionElement[_T], *order_by: _ColumnExpressionArgument[Any] | Any
) -> WithinGroup[_T]:
    return sqlalchemy.within_group(element, *order_by)


def col(column_expression: _T) -> Mapped[_T]:
    if not isinstance(column_expression, (ColumnClause, Column, InstrumentedAttribute)):
        raise RuntimeError(f"Not a SQLAlchemy column: {column_expression}")
    return column_expression  # type: ignore
