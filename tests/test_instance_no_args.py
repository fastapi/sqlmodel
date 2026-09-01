import pytest
from pydantic import ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_not_allow_instantiation_without_arguments(clear_sqlmodel):
    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        description: str | None = None

    with pytest.raises(ValidationError):
        Item()


def test_allow_instantiation_with_required_arguments(clear_sqlmodel):
    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        description: str | None = None

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        item = Item(name="Rick")
        db.add(item)
        db.commit()
        statement = select(Item)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(item.id, int)
    SQLModel.metadata.clear()
