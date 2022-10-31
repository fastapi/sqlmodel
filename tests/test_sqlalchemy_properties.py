from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Session, SQLModel, select


def test_hybrid_property(in_memory_engine):
    class Interval(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        length: float

        @hybrid_property
        def radius(self) -> float:
            return abs(self.length) / 2

        @radius.expression
        def radius(cls) -> float:
            return func.abs(cls.length) / 2

        class Config:
            arbitrary_types_allowed = True

    SQLModel.metadata.create_all(in_memory_engine)
    session = Session(in_memory_engine)

    interval = Interval(length=-2)
    assert interval.radius == 1

    session.add(interval)
    session.commit()
    interval_2 = session.exec(select(Interval)).all()[0]
    assert interval_2.radius == 1

    interval_3 = session.exec(select(Interval).where(Interval.radius == 1)).all()[0]
    assert interval_3.radius == 1

    intervals = session.exec(select(Interval).where(Interval.radius > 1)).all()
    assert len(intervals) == 0

    assert session.exec(select(Interval.radius + 1)).all()[0] == 2.0
