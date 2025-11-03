import re
import sys
from enum import Enum
from typing import Dict, Optional

import pytest
from sqlalchemy.orm.collections import attribute_keyed_dict
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


def test_attribute_keyed_dict_works(clear_sqlmodel):
    class Color(str, Enum):
        Orange = "Orange"
        Blue = "Blue"

    class Child(SQLModel, table=True):
        __tablename__ = "children"

        id: Optional[int] = Field(primary_key=True, default=None)
        parent_id: int = Field(foreign_key="parents.id")
        color: Color
        value: int

    class Parent(SQLModel, table=True):
        __tablename__ = "parents"

        id: Optional[int] = Field(primary_key=True, default=None)
        children_by_color: Dict[Color, Child] = Relationship(
            sa_relationship_kwargs={"collection_class": attribute_keyed_dict("color")}
        )

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        parent = Parent()
        session.add(parent)
        session.commit()
        session.refresh(parent)
        session.add(Child(parent_id=parent.id, color=Color.Orange, value=1))
        session.add(Child(parent_id=parent.id, color=Color.Blue, value=2))
        session.commit()
        session.refresh(parent)
        assert parent.children_by_color[Color.Orange].parent_id == parent.id
        assert parent.children_by_color[Color.Orange].color == Color.Orange
        assert parent.children_by_color[Color.Orange].value == 1
        assert parent.children_by_color[Color.Blue].parent_id == parent.id
        assert parent.children_by_color[Color.Blue].color == Color.Blue
        assert parent.children_by_color[Color.Blue].value == 2


# typing.Dict throws if it receives the wrong number of type arguments, but
# dict (3.10+) does not.
@pytest.skipif(sys.version_info < 3.10)
def test_dict_relationship_throws_on_missing_annotation_arg(clear_sqlmodel):
    class Color(str, Enum):
        Orange = "Orange"
        Blue = "Blue"

    class Child(SQLModel, table=True):
        __tablename__ = "children"

        id: Optional[int] = Field(primary_key=True, default=None)
        parent_id: int = Field(foreign_key="parents.id")
        color: Color
        value: int

    error_msg_re = re.escape(
        "Dict/Mapping relationship field 'children_by_color' must have both key and value type arguments (e.g., dict[str, Model])"
    )
    # No type args
    with pytest.raises(ValueError, match=error_msg_re):

        class Parent(SQLModel, table=True):
            __tablename__ = "parents"

            id: Optional[int] = Field(primary_key=True, default=None)
            children_by_color: dict[()] = Relationship(
                sa_relationship_kwargs={
                    "collection_class": attribute_keyed_dict("color")
                }
            )

    # One type arg
    with pytest.raises(ValueError, match=error_msg_re):

        class Parent(SQLModel, table=True):
            __tablename__ = "parents"

            id: Optional[int] = Field(primary_key=True, default=None)
            children_by_color: dict[Color] = Relationship(
                sa_relationship_kwargs={
                    "collection_class": attribute_keyed_dict("color")
                }
            )
