from typing import Any, cast

from sqlalchemy import Integer, String
from sqlmodel import Field, SQLModel


def test_sa_type_class() -> None:
    class Item(SQLModel, table=True):
        id: int = Field(primary_key=True, sa_type=Integer)

    id_column = cast(Any, Item).id
    assert isinstance(id_column.type, Integer)


def test_sa_type_instance() -> None:
    class Item(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str = Field(sa_type=String(50))

    name_column = cast(Any, Item).name
    assert isinstance(name_column.type, String)
    assert name_column.type.length == 50
