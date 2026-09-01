import pytest
from pydantic import ConfigDict, ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_frozen_non_table_model_creation(clear_sqlmodel):
    class HeroBase(SQLModel):
        model_config = ConfigDict(frozen=True)

        name: str
        age: int | None = None

    hero = HeroBase(name="Deadpond", age=30)

    assert hero.name == "Deadpond"
    assert hero.age == 30


def test_frozen_non_table_model_is_immutable(clear_sqlmodel):
    class HeroBase(SQLModel):
        model_config = ConfigDict(frozen=True)

        name: str
        age: int | None = None

    hero = HeroBase(name="Deadpond", age=30)

    with pytest.raises((ValidationError, TypeError)):
        hero.name = "Spider-Boy"  # type: ignore[misc]


def test_frozen_table_model_creation(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        model_config = ConfigDict(frozen=True)

        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

    hero = Hero(name="Deadpond", age=30)

    assert hero.name == "Deadpond"
    assert hero.age == 30


def test_frozen_table_model_persists_and_retrieves(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        model_config = ConfigDict(frozen=True)

        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        hero = Hero(name="Deadpond", age=30)
        session.add(hero)
        session.commit()
        session.refresh(hero)

    with Session(engine) as session:
        retrieved = session.exec(select(Hero)).one()
        assert retrieved.name == "Deadpond"
        assert retrieved.age == 30


def test_frozen_table_model_validate(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        model_config = ConfigDict(frozen=True)

        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

    hero = Hero.model_validate({"name": "Deadpond", "age": 30})

    assert hero.name == "Deadpond"
    assert hero.age == 30
