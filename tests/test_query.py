import pytest
from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel


def test_query(database_engine: Engine):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: int | None = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = database_engine

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
