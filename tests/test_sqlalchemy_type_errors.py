from typing import Any, Optional, Union

import pytest
from sqlmodel import Field, SQLModel


def test_type_list_breaks() -> None:
    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            tags: list[str]


def test_type_dict_breaks() -> None:
    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            tags: dict[str, Any]


def test_type_union_breaks() -> None:
    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            tags: Union[int, str]
