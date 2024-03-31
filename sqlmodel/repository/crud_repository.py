from typing import Any, Callable, Generic, Iterable, Optional, Type, TypeVar, get_args
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Engine, create_engine
from sqlalchemy.sql import text
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", SQLModel, BaseModel)
ID = TypeVar("ID", UUID, int)

import logging

logger = logging.getLogger(__name__)


class CrudRepository(Generic[ID, T]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.id_type, self.model_class = self._get_model_id_type_with_class()

    @classmethod
    def create_all_tables(cls, url: str) -> Engine:
        engine = create_engine(url, echo=False)
        SQLModel.metadata.create_all(engine)
        return engine

    @classmethod
    def _get_model_id_type_with_class(cls) -> tuple[Type[ID], Type[T]]:
        return get_args(tp=cls.__mro__[0].__orig_bases__[0])

    def _commit_operation_in_session(
        self, session_operation: Callable[[Session], None], session: Session
    ) -> bool:
        try:
            session_operation(session)
            session.commit()
        except Exception as error:
            logger.error(error)
            return False

        return True

    def _create_session(self) -> Session:
        return Session(self.engine, expire_on_commit=True)

    def find_by_id(self, id: ID) -> tuple[T, Session]:
        session = self._create_session()
        statement = select(self.model_class).where(self.model_class.id == id)  # type: ignore
        return (session.exec(statement).one(), session)

    def find_all_by_ids(self, ids: list[ID]) -> tuple[Iterable[T], Session]:
        session = self._create_session()
        statement = select(self.model_class).where(self.model_class.id in ids)  # type: ignore
        return (session.exec(statement).all(), session)

    def find_all(self) -> tuple[Iterable[T], Session]:
        session = self._create_session()
        statement = select(self.model_class)  # type: ignore
        return (session.exec(statement).all(), session)

    def save(self, entity: T, session: Optional[Session] = None) -> T:
        self._commit_operation_in_session(
            lambda session: session.add(entity), session or self._create_session()
        )
        return entity

    def save_all(
        self, entities: Iterable[T], session: Optional[Session] = None
    ) -> bool:
        return self._commit_operation_in_session(
            lambda session: session.add_all(entities), session or self._create_session()
        )

    def delete(self, entity: T, session: Optional[Session] = None) -> bool:
        return self._commit_operation_in_session(
            lambda session: session.delete(entity), session or self._create_session()
        )

    def delete_all(
        self, entities: Iterable[T], session: Optional[Session] = None
    ) -> bool:
        session = session or self._create_session()
        for entity in entities:
            session.delete(entity)
        session.commit()

        return True


def native_query(query: str, return_type: Type[T]) -> Any:
    def decorated(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(self: CrudRepository, **kwargs) -> T:
            with self.engine.connect() as connection:
                sql = text(query.format(**kwargs))
                query_result = connection.execute(sql)
                query_result_dicts = query_result.mappings().all()
                if return_type.__name__ == "Iterable":
                    cls_inside_inside_iterable = get_args(return_type)[0]
                    return [
                        cls_inside_inside_iterable.model_validate(query_result)
                        for query_result in query_result_dicts
                    ]  # type: ignore
                return return_type.model_validate(
                    list(query_result_dicts).pop()
                )  # Create an instance of the specified model class
            # return model_instance

        return wrapper

    return decorated  # type: ignore
