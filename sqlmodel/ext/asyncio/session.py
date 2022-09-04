from typing import Any, Mapping, Optional, Sequence, Type, TypeVar, Union, overload

from sqlalchemy import util
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine
from sqlalchemy.sql.base import Executable as _Executable
from sqlmodel.sql.base import Executable
from typing_extensions import Literal

from ...engine.result import Result, ScalarResult
from ...orm.session import Session
from ...sql.expression import Select, SelectOfScalar

_T = TypeVar("_T")
_TSelectParam = TypeVar("_TSelectParam")


class AsyncSession(_AsyncSession):
    sync_session_class = Session
    sync_session: Session

    def __init__(
        self,
        bind: Optional[Union[AsyncConnection, AsyncEngine]] = None,
        binds: Optional[Mapping[object, Union[AsyncConnection, AsyncEngine]]] = None,
        sync_session_class: Type[Session] = Session,
        **kw: Any,
    ):
        super().__init__(
            bind=bind,
            binds=binds,
            sync_session_class=sync_session_class,
            **kw,
        )

    @overload
    async def exec(
        self,
        statement: Select[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> Result[_TSelectParam]:
        ...

    @overload
    async def exec(
        self,
        statement: SelectOfScalar[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult[_TSelectParam]:
        ...

    async def exec(
        self,
        statement: Union[
            Select[_TSelectParam],
            SelectOfScalar[_TSelectParam],
            Executable[_TSelectParam],
        ],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> Union[Result[_TSelectParam], ScalarResult[_TSelectParam]]:
        results = super().execute(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw,
        )
        if isinstance(statement, SelectOfScalar):
            return (await results).scalars()
        return await results

    async def execute(
        self,
        statement: _Executable,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Optional[Mapping[str, Any]] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> Result[Any]:
        return await super().execute(
            statement=statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw,
        )

    async def get(
        self,
        entity: Type[_TSelectParam],
        ident: Any,
        options: Optional[Sequence[Any]] = None,
        populate_existing: bool = False,
        with_for_update: Optional[Union[Literal[True], Mapping[str, Any]]] = None,
        identity_token: Optional[Any] = None,
        execution_options: Optional[Mapping[Any, Any]] = util.EMPTY_DICT,
    ) -> Optional[_TSelectParam]:
        return await super().get(
            entity=entity,
            ident=ident,
            options=options,
            populate_existing=populate_existing,
            with_for_update=with_for_update,
            identity_token=identity_token,
            execution_options=execution_options,
        )
