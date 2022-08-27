from typing import Any, Mapping, Optional, Sequence, Type, TypeVar, Union, overload

from sqlalchemy import util
from sqlalchemy.orm import Query as _Query
from sqlalchemy.orm import Session as _Session
from sqlalchemy.sql.base import Executable as _Executable
from sqlmodel.sql.expression import Select, SelectOfScalar
from typing_extensions import Literal

from ..engine.result import Result, ScalarResult
from ..sql.base import Executable

_TSelectParam = TypeVar("_TSelectParam")


class Session(_Session):
    @overload
    def exec(
        self,
        statement: Select[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Result[_TSelectParam]:
        ...

    @overload
    def exec(
        self,
        statement: SelectOfScalar[_TSelectParam],
        *,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Mapping[str, Any] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> ScalarResult[_TSelectParam]:
        ...

    def exec(
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
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Union[Result[_TSelectParam], ScalarResult[_TSelectParam]]:
        results = super().execute(
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
            **kw,
        )
        if isinstance(statement, SelectOfScalar):
            return results.scalars()  # type: ignore
        return results  # type: ignore

    def execute(
        self,
        statement: _Executable,
        params: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]] = None,
        execution_options: Optional[Mapping[str, Any]] = util.EMPTY_DICT,
        bind_arguments: Optional[Mapping[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
        **kw: Any,
    ) -> Result[Any]:
        """
        🚨 You probably want to use `session.exec()` instead of `session.execute()`.

        This is the original SQLAlchemy `session.execute()` method that returns objects
        of type `Row`, and that you have to call `scalars()` to get the model objects.

        For example:

        ```Python
        heroes = session.execute(select(Hero)).scalars().all()
        ```

        instead you could use `exec()`:

        ```Python
        heroes = session.exec(select(Hero)).all()
        ```
        """
        return super().execute(  # type: ignore
            statement,
            params=params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            _parent_execute_state=_parent_execute_state,
            _add_event=_add_event,
            **kw,
        )

    def query(self, *entities: Any, **kwargs: Any) -> "_Query[Any]":
        """
        🚨 You probably want to use `session.exec()` instead of `session.query()`.

        `session.exec()` is SQLModel's own short version with increased type
        annotations.

        Or otherwise you might want to use `session.execute()` instead of
        `session.query()`.
        """
        return super().query(*entities, **kwargs)

    def get(
        self,
        entity: Type[_TSelectParam],
        ident: Any,
        options: Optional[Sequence[Any]] = None,
        populate_existing: bool = False,
        with_for_update: Optional[Union[Literal[True], Mapping[str, Any]]] = None,
        identity_token: Optional[Any] = None,
        execution_options: Optional[Mapping[Any, Any]] = util.EMPTY_DICT,
    ) -> Optional[_TSelectParam]:
        return super().get(
            entity,
            ident,
            options=options,
            populate_existing=populate_existing,
            with_for_update=with_for_update,
            identity_token=identity_token,
            execution_options=execution_options,
        )
