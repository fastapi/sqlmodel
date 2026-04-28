"""Mirrors sqlalchemy/test/orm/inheritance/test_basic.py :: FalseDiscriminatorTest, CascadeTest"""

from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy.orm import mapped_column
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_false_discriminator_on_sub():
    # mirrors FalseDiscriminatorTest.test_false_on_sub
    class DFoo(SQLModel, table=True):
        __tablename__ = "t_false_sub"
        id: Optional[int] = Field(default=None, primary_key=True)
        type: Optional[bool] = Field(
            default=None, sa_column=mapped_column(Boolean, nullable=True)
        )

        __mapper_args__ = {"polymorphic_on": "type", "polymorphic_identity": True}

    class DBar(DFoo):
        __mapper_args__ = {"polymorphic_identity": False}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        b1 = DBar()
        db.add(b1)
        db.commit()
        db.refresh(b1)
        assert b1.type is False

    with Session(engine) as db:
        result = db.exec(select(DFoo)).one()
        assert isinstance(result, DBar)


def test_false_discriminator_on_base():
    # mirrors FalseDiscriminatorTest.test_false_on_base
    class Ding(SQLModel, table=True):
        __tablename__ = "t_false_base"
        id: Optional[int] = Field(default=None, primary_key=True)
        type: Optional[bool] = Field(
            default=None, sa_column=mapped_column(Boolean, nullable=True)
        )

        __mapper_args__ = {"polymorphic_on": "type", "polymorphic_identity": False}

    class Bat(Ding):
        __mapper_args__ = {"polymorphic_identity": True}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        d1 = Ding()
        db.add(d1)
        db.commit()
        db.refresh(d1)
        assert d1.type is False

    with Session(engine) as db:
        assert db.exec(select(Ding)).one() is not None


def test_cascade_delete_follows_subclass_mapper():
    # mirrors CascadeTest.test_cascade
    class Note(SQLModel, table=True):
        __tablename__ = "cascade_note"
        id: Optional[int] = Field(default=None, primary_key=True)
        data: str
        item_id: Optional[int] = Field(default=None, foreign_key="cascade_item.id")

    class Item(SQLModel, table=True):
        __tablename__ = "cascade_item"
        id: Optional[int] = Field(default=None, primary_key=True)
        type: str = Field(default="item")
        data: str
        notes: list[Note] = Relationship(sa_relationship_kwargs={"cascade": "all"})

        __mapper_args__ = {
            "polymorphic_on": "type",
            "polymorphic_identity": "item",
        }

    class SubItem(Item):
        __tablename__ = "cascade_subitem"
        id: Optional[int] = Field(
            default=None, primary_key=True, foreign_key="cascade_item.id"
        )
        extra: str = Field(default="")

        __mapper_args__ = {"polymorphic_identity": "subitem"}

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        sub = SubItem(data="hello", extra="world")
        db.add(sub)
        db.flush()
        sub_id = sub.id
        db.add(Note(data="note1", item_id=sub_id))
        db.add(Note(data="note2", item_id=sub_id))
        db.commit()

    with Session(engine) as db:
        sub = db.get(SubItem, sub_id)
        _ = sub.notes
        db.delete(sub)
        db.commit()

    with Session(engine) as db:
        assert db.exec(select(Note)).all() == []
        assert db.exec(select(Item)).all() == []


