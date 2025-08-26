from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import aliased
from sqlmodel import Field, Relationship, Session, SQLModel, select


def test_sa_multi_relationship_alias(clear_sqlmodel) -> None:
    class Team(SQLModel, table=True):
        """Team model."""

        __tablename__ = "team_multi"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    class Hero(SQLModel, table=True):
        """Hero model."""

        __tablename__ = "hero_multi"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        winter_team_id: Optional[int] = Field(default=None, foreign_key="team_multi.id")
        winter_team: Optional[Team] = Relationship(
            sa_relationship_kwargs={"primaryjoin": "Hero.winter_team_id == Team.id"}
        )
        summer_team_id: Optional[int] = Field(default=None, foreign_key="team_multi.id")
        summer_team: Optional[Team] = Relationship(
            sa_relationship_kwargs={"primaryjoin": "Hero.summer_team_id == Team.id"}
        )

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        blue_team = Team(name="Blue")
        red_team = Team(name="Red")
        session.add_all([blue_team, red_team])
        session.commit()
        session.refresh(blue_team)
        session.refresh(red_team)

        hero1 = Hero(
            name="dual_team", winter_team_id=blue_team.id, summer_team_id=red_team.id
        )
        session.add(hero1)
        hero2 = Hero(
            name="single_team", winter_team_id=red_team.id, summer_team_id=red_team.id
        )
        session.add_all([hero1, hero2])
        session.commit()

        winter_alias = aliased(Team)
        summer_alias = aliased(Team)
        result = session.exec(
            select(Hero)
            .join(winter_alias, onclause=Hero.winter_team_id == winter_alias.id)
            .where(winter_alias.name == "Blue")
            .join(summer_alias, onclause=Hero.summer_team_id == summer_alias.id)
            .where(summer_alias.name == "Red")
        ).all()
        assert len(result) == 1
        assert result[0].name == "dual_team"
