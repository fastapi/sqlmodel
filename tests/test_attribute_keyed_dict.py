from enum import StrEnum

from sqlalchemy.orm.collections import attribute_keyed_dict
from sqlmodel import Field, Index, Relationship, Session, SQLModel, create_engine


def test_attribute_keyed_dict_works(clear_sqlmodel):
    class Color(StrEnum):
        Orange = "Orange"
        Blue = "Blue"

    class Child(SQLModel, table=True):
        __tablename__ = "children"
        __table_args__ = (
            Index("ix_children_parent_id_color", "parent_id", "color", unique=True),
        )

        id: int | None = Field(primary_key=True, default=None)
        parent_id: int = Field(foreign_key="parents.id")
        color: Color
        value: int

    class Parent(SQLModel, table=True):
        __tablename__ = "parents"

        id: int | None = Field(primary_key=True, default=None)
        children_by_color: dict[Color, Child] = Relationship(
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
