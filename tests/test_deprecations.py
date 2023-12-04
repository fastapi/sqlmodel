import pytest
from sqlmodel import SQLModel


class Item(SQLModel):
    name: str


class SubItem(Item):
    password: str


def test_deprecated_from_orm_inheritance():
    new_item = SubItem(name="Hello", password="secret")
    with pytest.warns(DeprecationWarning):
        item = Item.from_orm(new_item)
    assert item.name == "Hello"
    assert not hasattr(item, "password")


def test_deprecated_parse_obj():
    with pytest.warns(DeprecationWarning):
        item = Item.parse_obj({"name": "Hello"})
    assert item.name == "Hello"


def test_deprecated_dict():
    with pytest.warns(DeprecationWarning):
        data = Item(name="Hello").dict()
    assert data == {"name": "Hello"}
