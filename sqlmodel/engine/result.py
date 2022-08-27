from typing import Generic, Iterator, List, Optional, TypeVar

from sqlalchemy.engine.result import Result as _Result
from sqlalchemy.engine.result import ScalarResult as _ScalarResult

_T = TypeVar("_T")


class ScalarResult(_ScalarResult, Generic[_T]):
    def all(self) -> List[_T]:
        return super().all()

    def partitions(self, size: Optional[int] = None) -> Iterator[List[_T]]:
        return super().partitions(size)

    def fetchall(self) -> List[_T]:
        return super().fetchall()

    def fetchmany(self, size: Optional[int] = None) -> List[_T]:
        return super().fetchmany(size)

    def __iter__(self) -> Iterator[_T]:
        return super().__iter__()

    def __next__(self) -> _T:
        return super().__next__()  # type: ignore

    def first(self) -> Optional[_T]:
        return super().first()

    def one_or_none(self) -> Optional[_T]:
        return super().one_or_none()

    def one(self) -> _T:
        return super().one()  # type: ignore


class Result(_Result, Generic[_T]):
    def scalars(self, index: int = 0) -> ScalarResult[_T]:
        return super().scalars(index)  # type: ignore

    def __iter__(self) -> Iterator[_T]:  # type: ignore
        return super().__iter__()  # type: ignore

    def __next__(self) -> _T:  # type: ignore
        return super().__next__()  # type: ignore

    def partitions(self, size: Optional[int] = None) -> Iterator[List[_T]]:  # type: ignore
        return super().partitions(size)  # type: ignore

    def fetchall(self) -> List[_T]:  # type: ignore
        return super().fetchall()  # type: ignore

    def fetchone(self) -> Optional[_T]:  # type: ignore
        return super().fetchone()  # type: ignore

    def fetchmany(self, size: Optional[int] = None) -> List[_T]:  # type: ignore
        return super().fetchmany()  # type: ignore

    def all(self) -> List[_T]:  # type: ignore
        return super().all()  # type: ignore

    def first(self) -> Optional[_T]:  # type: ignore
        return super().first()  # type: ignore

    def one_or_none(self) -> Optional[_T]:  # type: ignore
        return super().one_or_none()  # type: ignore

    def scalar_one(self) -> _T:
        return super().scalar_one()  # type: ignore

    def scalar_one_or_none(self) -> Optional[_T]:
        return super().scalar_one_or_none()

    def one(self) -> _T:  # type: ignore
        return super().one()  # type: ignore

    def scalar(self) -> Optional[_T]:
        return super().scalar()
