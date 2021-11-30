from typing import Any, Mapping, Optional, Sequence, TypeVar, Union

from sqlalchemy import util
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import engine
from sqlalchemy.ext.asyncio.engine import AsyncConnection, AsyncEngine
from sqlalchemy.util.concurrency import greenlet_spawn
from sqlmodel.sql.base import Executable

from ...engine.result import ScalarResult
from ...orm.session import Session
from ...sql.expression import Select

_T = TypeVar("_T")


class AsyncSession(_AsyncSession):
    sync_session: Session

    def __init__(
        self,
        bind: Optional[Union[AsyncConnection, AsyncEngine]] = None,
        binds: Optional[Mapping[object, Union[AsyncConnection, AsyncEngine]]] = None,
        **kw: Any,
    ):
        # All the same code of the original AsyncSession
        kw["future"] = True
        if bind:
            self.bind = bind
            bind = engine._get_sync_engine_or_connection(bind)  # type: ignore

        if binds:
            self.binds = binds
            binds = {
                key: engine._get_sync_engine_or_connection(b)  # type: ignore
                for key, b in binds.items()
            }

        self.sync_session = self._proxied = self._assign_proxied(  # type: ignore
            Session(bind=bind, binds=binds, **kw)  # type: ignore
        )

    async def exec(
        self,
        statement: Union[Select[_T], Executable[_T]],
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[Any, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        **kw: Any,
    ) -> ScalarResult[_T]:
        # TODO: the documentation says execution_options accepts a dict, but only
        # util.immutabledict has the union() method. Is this a bug in SQLAlchemy?
        execution_options = execution_options.union({"prebuffer_rows": True})  # type: ignore

        return await greenlet_spawn(
            self.sync_session.exec,
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw,
        )
