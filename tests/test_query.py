import pytest
from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select


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


def test_exec_multi_column_select(database_engine: Engine):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    engine = database_engine
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        statement = select(Hero.id, Hero.name)
        result = session.exec(statement)
        assert result is not None
        rows = result.all()
        assert len(rows) == 1
        assert rows[0] == (hero_1.id, "Deadpond")


def test_exec_update_statement(database_engine: Engine):
    from sqlalchemy import update

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    engine = database_engine
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        statement = update(Hero).where(Hero.name == "Deadpond").values(name="Alivepond")
        cursor_result = session.exec(statement)
        assert cursor_result is not None
        assert cursor_result.rowcount == 1
        session.commit()

    with Session(engine) as session:
        updated = session.exec(select(Hero).where(Hero.id == hero_1.id)).first()
        assert updated is not None
        assert updated.name == "Alivepond"
