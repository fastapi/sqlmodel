"""Test for Dict relationship recursion bug fix."""
from typing import Dict

import pytest
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlmodel import Field, Relationship, SQLModel


def test_dict_relationship_pattern():
    """Test that Dict relationships with attribute_mapped_collection work."""

    # Create a minimal reproduction of the pattern
    # This should not raise a RecursionError

    class TestChild(SQLModel, table=True):
        __tablename__ = "test_child"
        id: int = Field(primary_key=True)
        key: str = Field(nullable=False)
        parent_id: int = Field(foreign_key="test_parent.id")
        parent: "TestParent" = Relationship(back_populates="children")

    class TestParent(SQLModel, table=True):
        __tablename__ = "test_parent"
        id: int = Field(primary_key=True)
        children: Dict[str, "TestChild"] = Relationship(
            back_populates="parent",
            sa_relationship_kwargs={
                "collection_class": attribute_mapped_collection("key")
            },
        )

    # If we got here without RecursionError, the bug is fixed
    assert TestParent.__tablename__ == "test_parent"
    assert TestChild.__tablename__ == "test_child"


def test_dict_relationship_with_optional():
    """Test that Optional[Dict[...]] relationships also work."""
    from typing import Optional

    class Child(SQLModel, table=True):
        __tablename__ = "child"
        id: int = Field(primary_key=True)
        key: str = Field(nullable=False)
        parent_id: int = Field(foreign_key="parent.id")
        parent: Optional["Parent"] = Relationship(back_populates="children")

    class Parent(SQLModel, table=True):
        __tablename__ = "parent"
        id: int = Field(primary_key=True)
        children: Optional[Dict[str, "Child"]] = Relationship(
            back_populates="parent",
            sa_relationship_kwargs={
                "collection_class": attribute_mapped_collection("key")
            },
        )

    # If we got here without RecursionError, the bug is fixed
    assert Parent.__tablename__ == "parent"
    assert Child.__tablename__ == "child"
