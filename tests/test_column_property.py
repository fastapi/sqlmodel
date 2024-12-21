from typing import List, Optional

from sqlalchemy import case, create_engine, func
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import Field, Relationship, Session, SQLModel, select


def test_query(clear_sqlmodel):
    class Item(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        value: float
        hero_id: int = Field(foreign_key="hero.id")
        hero: "Hero" = Relationship(back_populates="items")

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        items: List[Item] = Relationship(back_populates="hero")

        @declared_attr
        def total_items(cls):
            return column_property(cls._total_items_expression())

        @classmethod
        def _total_items_expression(cls):
            return (
                select(func.coalesce(func.sum(Item.value), 0))
                .where(Item.hero_id == cls.id)
                .correlate_except(Item)
                .label("total_items")
            )

        @declared_attr
        def status(cls):
            return column_property(
                select(
                    case(
                        (cls._total_items_expression() > 0, "active"), else_="inactive"
                    )
                ).scalar_subquery()
            )

    hero_1 = Hero(name="Deadpond")
    hero_2 = Hero(name="Spiderman")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

    item_1 = Item(value=1.0, hero_id=hero_1.id)
    item_2 = Item(value=2.0, hero_id=hero_1.id)

    with Session(engine) as session:
        session.add(item_1)
        session.add(item_2)
        session.commit()
        session.refresh(item_1)
        session.refresh(item_2)

    with Session(engine) as session:
        hero_statement = select(Hero).where(Hero.total_items > 0.0)
        hero = session.exec(hero_statement).first()
        assert hero.name == "Deadpond"
        assert hero.total_items == 3.0
        assert hero.status == "active"

    with Session(engine) as session:
        hero_statement = select(Hero).where(
            Hero.status == "inactive",
        )
        hero = session.exec(hero_statement).first()
        assert hero.name == "Spiderman"
        assert hero.total_items == 0.0
        assert hero.status == "inactive"
