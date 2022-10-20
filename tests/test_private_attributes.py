from typing import Optional

from pydantic import PrivateAttr
from sqlmodel import Field, SQLModel


def test_private_attribute():
    class Hero(SQLModel, table=True):
        primary_key: Optional[int] = Field(
            default=None,
            primary_key=True,
        )
        _private_attribute: str = PrivateAttr(default="my_private_attribute")

    hero = Hero()
    assert hero._private_attribute == "my_private_attribute"
    assert "primary_key" in hero.dict()
    assert "_private_attribute" not in hero.dict()
