from typing import Annotated

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_annotated_relationship_with_default() -> None:
    class Team(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]

        heroes: Annotated[list["Hero"], Relationship(back_populates="team")] = []  # noqa: RUF012

    class Hero(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]
        team_id: Annotated[int | None, Field(foreign_key="team.id")] = None
        team: Annotated[Team | None, Relationship(back_populates="heroes")] = None

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        team = Team(name="Preventers")
        hero = Hero(name="Deadpond", team=team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.team is not None
        assert hero.team.name == "Preventers"
        team_db = session.exec(select(Team)).one()
        assert [h.name for h in team_db.heroes] == ["Deadpond"]


def test_annotated_relationship_without_default() -> None:
    class Team(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]

        heroes: Annotated[list["Hero"], Relationship(back_populates="team")]

    class Hero(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]
        team_id: Annotated[int | None, Field(foreign_key="team.id")] = None
        team: Annotated[Team | None, Relationship(back_populates="heroes")]

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        team = Team(name="Z-Force")
        hero = Hero(name="Spider-Boy", team=team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.team is not None
        assert hero.team.name == "Z-Force"


def test_annotated_mapped_relationship() -> None:
    class Team(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]

        heroes: Annotated[
            Mapped[list["Hero"]], Relationship(back_populates="team")
        ] = []  # noqa: RUF012

    class Hero(SQLModel, table=True):
        id: Annotated[int | None, Field(primary_key=True)] = None
        name: Annotated[str, Field(index=True)]
        team_id: Annotated[int | None, Field(foreign_key="team.id")] = None
        team: Annotated[Mapped[Team | None], Relationship(back_populates="heroes")] = (
            None
        )

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        team = Team(name="Avengers")
        hero = Hero(name="Iron Man", team=team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.team is not None
        assert hero.team.name == "Avengers"
