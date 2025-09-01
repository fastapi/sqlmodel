from typing import Optional

from sqlalchemy.orm import aliased
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    winter_team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    winter_team: Optional[Team] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Hero.winter_team_id"}
    )
    summer_team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    summer_team: Optional[Team] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Hero.summer_team_id"}
    )


sqlite_file_name = ":memory:"
sqlite_url = f"sqlite:///{sqlite_file_name}"
mysql_url = "mysql+pymysql://root@127.0.0.1/test"

engine = create_engine(mysql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            winter_team=team_preventers,
            summer_team=team_z_force,
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            winter_team=team_preventers,
            summer_team=team_preventers,
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)


def select_heroes():
    with Session(engine) as session:
        winter_alias = aliased(Team)

        # Heros with winter team as the Preventers using "aliases" and "onclause"
        result = session.exec(
            select(Hero)
            .join(winter_alias, onclause=Hero.winter_team_id == winter_alias.id)
            .where(winter_alias.name == "Preventers")
        )
        """
        SQL Looks like:

        SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.winter_team_id, hero.summer_team_id
        FROM hero JOIN team AS team_1 ON hero.winter_team_id = team_1.id
        WHERE team_1.name = ?

        """
        heros = result.all()
        print("Heros with Preventers as their winter team:", heros)

        # Heros with Preventers as their winter team and Z-Force as their summer team using "has" function.
        result = session.exec(
            select(Hero)
            .where(Hero.winter_team.has(Team.name == "Preventers"))
            .where(Hero.summer_team.has(Team.name == "Z-Force"))
        )
        """
        SQL Looks like:

        SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.winter_team_id, hero.summer_team_id
        FROM hero
        WHERE (
          EXISTS (
            SELECT 1 FROM team
            WHERE team.id = hero.winter_team_id AND team.name = ?
          )
        ) AND (
          EXISTS (
            SELECT 1 FROM team
            WHERE team.id = hero.summer_team_id AND team.name = ?
          )
        )
        """
        heros = result.all()
        print(
            "Heros with Preventers as their winter and Z-Force as their summer team:",
            heros,
        )
        assert heros[0].name == "Deadpond"


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
