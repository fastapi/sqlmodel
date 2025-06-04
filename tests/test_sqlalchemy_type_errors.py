from typing import Any, Dict, List, Optional, Union

import pytest
from sqlmodel import Field, SQLModel


def test_type_list_works(clear_sqlmodel) -> None:
    """Test that List types are now supported in SQLModel table classes."""

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        tags: List[str]

    # Should not raise an error and should create a table column
    assert "tags" in Hero.__table__.columns

    # Can create an instance
    hero = Hero(tags=["tag1", "tag2"])
    assert hero.tags == ["tag1", "tag2"]


def test_type_dict_works(clear_sqlmodel) -> None:
    """Test that Dict types are now supported in SQLModel table classes."""

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        tags: Dict[str, Any]

    # Should not raise an error and should create a table column
    assert "tags" in Hero.__table__.columns

    # Can create an instance
    hero = Hero(tags={"key": "value"})
    assert hero.tags == {"key": "value"}


def test_type_union_breaks(clear_sqlmodel) -> None:
    """Test that Union types still raise ValueError in SQLModel table classes."""
    with pytest.raises(ValueError):

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            tags: Union[int, str]
