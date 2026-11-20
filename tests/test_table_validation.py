import pytest
from pydantic import ValidationError
from sqlalchemy import Engine
from sqlmodel import Field, Relationship, Session, SQLModel, select


def test_table_model_validates_field_types():
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int

    with pytest.raises(ValidationError) as exc_info:
        Hero(name="Spider-Boy", age="not-an-integer")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("age",)


def test_table_model_validates_field_constraints():
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str = Field(min_length=2, max_length=20)
        power_level: int = Field(gt=0)

    with pytest.raises(ValidationError):
        Hero(name="A", power_level=10)

    with pytest.raises(ValidationError):
        Hero(name="Spider-Boy", power_level=-5)


def test_table_model_coerces_and_persists_in_db(database_engine: Engine):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int

    SQLModel.metadata.create_all(database_engine)
    hero = Hero(name="Spider-Boy", age="25")  # type: ignore[arg-type]
    assert hero.age == 25
    assert isinstance(hero.age, int)

    with Session(database_engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        saved = session.exec(select(Hero)).one()

    assert saved.id is not None
    assert saved.name == "Spider-Boy"
    assert saved.age == 25


def test_table_model_validates_with_relationships(database_engine: Engine):
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    SQLModel.metadata.create_all(database_engine)
    team = Team(name="Preventers")

    with pytest.raises(ValidationError):
        Hero(name="Spider-Boy", age="invalid", team=team)  # type: ignore[arg-type]

    hero = Hero(name="Spider-Boy", age="21", team=team)  # type: ignore[arg-type]
    assert hero.age == 21
    assert hero.team is team

    with Session(database_engine) as session:
        session.add(hero)
        session.commit()
        saved_hero = session.exec(select(Hero)).one()
        assert saved_hero.team is not None
        assert saved_hero.team.name == "Preventers"
