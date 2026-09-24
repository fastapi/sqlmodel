import pytest
from pydantic import ValidationError
from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select


def test_allow_instantiation_without_arguments(database_engine: Engine):
    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        description: str | None = None

    engine = database_engine
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        item = Item()
        item.name = "Rick"
        db.add(item)
        db.commit()
        statement = select(Item)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(item.id, int)


def test_not_allow_instantiation_without_arguments_if_not_table():
    class Item(SQLModel):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        description: str | None = None

    with pytest.raises(ValidationError):
        Item()
