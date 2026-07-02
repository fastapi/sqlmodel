from typing import Annotated, NewType
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def test_field_is_newtype() -> None:
    NewId = NewType("NewId", UUID)

    class Item(SQLModel, table=True):
        id: NewId = Field(default_factory=uuid4, primary_key=True)

    item = Item()
    assert isinstance(item.id, UUID)


def test_field_is_recursive_newtype() -> None:
    NewId1 = NewType("NewId1", int)
    NewId2 = NewType("NewId2", NewId1)
    NewId3 = NewType("NewId3", NewId2)

    class Item(SQLModel, table=True):
        id: NewId3 = Field(primary_key=True)

    item = Item(id=NewId3(NewId2(NewId1(3))))
    assert isinstance(item.id, int)
    assert item.id == 3, item.id


def test_field_is_newtype_and_annotated() -> None:
    NewId = NewType("NewId", UUID)

    class Item(SQLModel, table=True):
        id: Annotated[NewId, Field(primary_key=True)] = NewId(uuid4())

    item = Item()
    assert isinstance(item.id, UUID)
