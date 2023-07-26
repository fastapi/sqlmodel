from typing import Generic, Iterator, Optional, Sequence, Tuple, TypeVar

from sqlalchemy.engine.result import Result as _Result
from sqlalchemy.engine.result import ScalarResult as _ScalarResult

_T = TypeVar("_T")


class ScalarResult(_ScalarResult[_T], Generic[_T]):
    def all(self) -> Sequence[_T]:
        return super().all()

    def partitions(self, size: Optional[int] = None) -> Iterator[Sequence[_T]]:
        return super().partitions(size)

    def fetchall(self) -> Sequence[_T]:
        return super().fetchall()

    def fetchmany(self, size: Optional[int] = None) -> Sequence[_T]:
        return super().fetchmany(size)

    def __iter__(self) -> Iterator[_T]:
        return super().__iter__()

    def __next__(self) -> _T:
        return super().__next__()

    def first(self) -> Optional[_T]:
        return super().first()

    def one_or_none(self) -> Optional[_T]:
        return super().one_or_none()

    def one(self) -> _T:
        return super().one()


class Result(_Result[Tuple[_T]], Generic[_T]):
    ...
