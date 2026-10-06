from collections.abc import Mapping, Sequence
from typing import (
    Any,
    TypeVar,
    cast,
    overload,
)

from sqlalchemy import util
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.interfaces import _CoreAnyExecuteParams
from sqlalchemy.engine.result import Result, ScalarResult, TupleResult
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio.result import _ensure_sync_result
from sqlalchemy.ext.asyncio.session import _EXECUTE_OPTIONS
from sqlalchemy.orm._typing import OrmExecuteOptionsParameter
from sqlalchemy.sql.base import Executable as _Executable
from sqlalchemy.sql.dml import UpdateBase
from sqlalchemy.util.concurrency import greenlet_spawn
from typing_extensions import TypeVarTuple, Unpack, deprecated

from ...orm.session import Session
from ...sql.base import Executable
from ...sql.expression import Select, SelectOfScalar

_TSelectParam = TypeVar("_TSelectParam", bound=Any)
_Ts = TypeVarTuple("_Ts")


class AsyncSession(_AsyncSession):
    sync_session_class: type[Session] = Session
    sync_session: Session

    @overload
    async def exec(
        self,
        statement: Select[Unpack[_Ts]],
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> TupleResult[tuple[Unpack[_Ts]]]: ...

    @overload
    async def exec(
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
    async def exec(
        self,
        statement: UpdateBase,
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> CursorResult[Unpack[tuple[Any, ...]]]: ...

    async def exec(
        self,
        statement: Select[Unpack[_Ts]]
        | SelectOfScalar[_TSelectParam]
        | Executable[_TSelectParam]
        | UpdateBase,
        *,
        params: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> (
        TupleResult[tuple[Unpack[_Ts]]]
        | ScalarResult[_TSelectParam]
        | CursorResult[Unpack[tuple[Any, ...]]]
    ):
        if execution_options:
            execution_options = util.immutabledict(execution_options).union(
                _EXECUTE_OPTIONS
            )
        else:
            execution_options = _EXECUTE_OPTIONS

        result = await greenlet_spawn(
            self.sync_session.exec,
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
        )
        result_value = await _ensure_sync_result(
            cast(Result[Unpack[tuple[Any, ...]]], result), self.exec
        )
        return result_value  # type: ignore

    @deprecated(
        """
        🚨 You probably want to use `session.exec()` instead of `session.execute()`.

        This is the original SQLAlchemy `session.execute()` method that returns objects
        of type `Row`, on which you have to call `scalars()` to get the model objects.

        For example:

        ```Python
        result = await session.execute(select(Hero))
        heroes = result.scalars().all()
        ```

        Instead, you could use `exec()`:

        ```Python
        result = await session.exec(select(Hero))
        heroes = result.all()
        ```
        """
    )
    async def execute(
        self,
        statement: _Executable,
        params: _CoreAnyExecuteParams | None = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: dict[str, Any] | None = None,
        _parent_execute_state: Any | None = None,
        _add_event: Any | None = None,
    ) -> Result[Unpack[tuple[Any, ...]]]:
        """
        🚨 You probably want to use `session.exec()` instead of `session.execute()`.

        This is the original SQLAlchemy `session.execute()` method that returns objects
        of type `Row`, on which you have to call `scalars()` to get the model objects.

        For example:

        ```Python
        result = await session.execute(select(Hero))
        heroes = result.scalars().all()
        ```

        Instead, you could use `exec()`:

        ```Python
        result = await session.exec(select(Hero))
        heroes = result.all()
        ```
        """
        return await super().execute(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
        )
