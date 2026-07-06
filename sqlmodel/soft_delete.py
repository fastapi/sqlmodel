from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any, ClassVar, TypeVar, overload

from sqlalchemy import util
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.result import ScalarResult, TupleResult
from sqlalchemy.sql.dml import UpdateBase

from .main import Field
from .orm.session import Session
from .sql.base import Executable
from .sql.expression import Select, SelectOfScalar

_TSelectParam = TypeVar("_TSelectParam", bound=Any)


class SoftDeleteMixin:
    __soft_delete_field__: ClassVar[str] = "deleted_at"

    deleted_at: datetime | None = Field(default=None)


def get_soft_delete_field(model: type[Any]) -> str | None:
    field_name = getattr(model, "__soft_delete_field__", None)
    if not isinstance(field_name, str):
        return None
    if not hasattr(model, field_name):
        return None
    return field_name


class SoftDeleteSession(Session):
    def delete(self, instance: Any, hard_delete: bool = False) -> None:
        field_name = get_soft_delete_field(type(instance))
        if not hard_delete and field_name is not None:
            setattr(instance, field_name, datetime.now(timezone.utc))
            self.add(instance)
            return None
        return super().delete(instance)

    @overload
    def exec(
        self,
        statement: Select[_TSelectParam],
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> TupleResult[_TSelectParam]: ...

    @overload
    def exec(
        self,
        statement: SelectOfScalar[_TSelectParam],
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> ScalarResult[_TSelectParam]: ...

    @overload
    def exec(
        self,
        statement: UpdateBase,
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> CursorResult[Any]: ...

    def exec(
        self,
        statement: Select[_TSelectParam]
        | SelectOfScalar[_TSelectParam]
        | Executable[_TSelectParam]
        | UpdateBase,
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> TupleResult[_TSelectParam] | ScalarResult[_TSelectParam] | CursorResult[Any]:
        statement = self._filter_soft_deleted(statement)
        return super().exec(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
        )

    def _filter_soft_deleted(self, statement: Any) -> Any:
        if statement.get_execution_options().get("include_deleted"):
            return statement

        models: set[type[Any]] = set()
        for description in getattr(statement, "column_descriptions", ()):
            model = description.get("entity")
            if isinstance(model, type):
                models.add(model)

        for model in models:
            field_name = get_soft_delete_field(model)
            if field_name is not None:
                statement = statement.where(getattr(model, field_name).is_(None))
        return statement
