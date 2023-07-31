from typing import Optional

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlmodel import Field, SQLModel


def test_allow_instantiation_without_arguments(clear_sqlmodel):
    class Item(SQLModel):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        description: Optional[str] = None

        class Config:
            table = True

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        item = Item()
        item.name = "Rick"
        db.add(item)
        db.commit()
        result = db.execute(select(Item)).scalars().all()
    assert len(result) == 1
    assert isinstance(item.id, int)
    SQLModel.metadata.clear()
