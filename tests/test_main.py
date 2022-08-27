from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


def test_should_allow_duplicate_row_if_unique_constraint_is_not_passed(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        session.add(hero_2)
        session.commit()
        session.refresh(hero_2)

    with Session(engine) as session:
        heroes = session.query(Hero).all()
        assert len(heroes) == 2
        assert heroes[0].name == heroes[1].name


def test_should_allow_duplicate_row_if_unique_constraint_is_false(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str = Field(unique=False)
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        session.add(hero_2)
        session.commit()
        session.refresh(hero_2)

    with Session(engine) as session:
        heroes = session.query(Hero).all()
        assert len(heroes) == 2
        assert heroes[0].name == heroes[1].name


def test_should_raise_exception_when_try_to_duplicate_row_if_unique_constraint_is_true(
    clear_sqlmodel,
):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str = Field(unique=True)
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with pytest.raises(IntegrityError):
        with Session(engine) as session:
            session.add(hero_2)
            session.commit()
            session.refresh(hero_2)
