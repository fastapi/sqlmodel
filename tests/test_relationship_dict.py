"""
Regression test for: model_validate with a dict containing relationship keys
silently drops the relationship data.

Root cause: sqlmodel_validate in _compat.py uses getattr(use_obj, key, Undefined)
to extract relationship values. When use_obj is a dict, getattr finds no attribute
named e.g. "heroes", returning Undefined, so relationships are never set.

Fix: use dict.get() when use_obj is a dict instance.
"""

from sqlalchemy.orm import selectinload
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_model_validate_dict_populates_relationships():
    """Relationships passed as dict keys to model_validate should be set."""

    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    heroes = [Hero(name="Deadpond"), Hero(name="Spider-Boy")]
    team = Team.model_validate({"name": "Z-Force", "heroes": heroes})

    assert len(team.heroes) == 2, (
        "model_validate with a dict should populate relationship fields"
    )


def test_model_validate_dict_relationships_persisted():
    """Relationships set via model_validate dict should be saved and loadable."""

    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    heroes = [Hero(name="Deadpond"), Hero(name="Spider-Boy")]
    team = Team.model_validate({"name": "Z-Force", "heroes": heroes})

    with Session(engine) as session:
        session.add(team)
        session.commit()

    with Session(engine) as session:
        loaded = session.exec(
            select(Team).options(selectinload(Team.heroes))  # type: ignore[arg-type]
        ).first()
        assert loaded is not None
        assert len(loaded.heroes) == 2
