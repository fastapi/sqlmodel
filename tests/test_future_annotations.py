from __future__ import annotations

from typing import Annotated

from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_model_with_future_annotations(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: str
        secret_name: str
        age: int | None = None

    hero = Hero(name="Deadpond", secret_name="Dive Wilson", age=25)

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)

        assert hero.id is not None
        assert hero.name == "Deadpond"
        assert hero.secret_name == "Dive Wilson"
        assert hero.age == 25

    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        assert len(heroes) == 1
        assert heroes[0].name == "Deadpond"


def test_model_with_string_annotations(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: str

    class Player(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: str
        team_id: Annotated[int | None, Field(foreign_key="team.id")] = None

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    team = Team(name="Champions")
    player = Player(name="Alice", team_id=None)

    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)

        player.team_id = team.id
        session.add(player)
        session.commit()
        session.refresh(player)

        assert team.id is not None
        assert player.team_id == team.id
