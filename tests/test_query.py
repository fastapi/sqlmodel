from typing import Optional

import pytest
from sqlmodel import Field, Session, SQLModel, create_engine


def test_query(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        with pytest.warns(DeprecationWarning):
            query_hero = session.query(Hero).first()
        assert query_hero
        assert query_hero.name == hero_1.name
