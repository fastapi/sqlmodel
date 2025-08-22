from sqlalchemy.orm import aliased
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    winter_team_id: int | None = Field(default=None, foreign_key="team.id")
    winter_team: Team | None = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Hero.winter_team_id == Team.id"}
    )
    summer_team_id: int | None = Field(default=None, foreign_key="team.id")
    summer_team: Team | None = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Hero.summer_team_id == Team.id"}
    )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


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

        # Heros with winter team as the Preventers
        result = session.exec(
            select(Hero)
            .join(winter_alias, onclause=Hero.winter_team_id == winter_alias.id)
            .where(winter_alias.name == "Preventers")
        )
        heros = result.all()
        print("Heros with Preventers as their winter team:", heros)
        assert len(heros) == 2

        summer_alias = aliased(Team)

        # Heros with Preventers as their winter team and Z-Force as their summer team
        result = session.exec(
            select(Hero)
            .join(winter_alias, onclause=Hero.winter_team_id == winter_alias.id)
            .where(winter_alias.name == "Preventers")
            .join(summer_alias, onclause=Hero.summer_team_id == summer_alias.id)
            .where(summer_alias.name == "Z-Force")
        )
        heros = result.all()
        print(
            "Heros with Preventers as their winter and Z-Force as their summer team:",
            heros,
        )
        assert len(heros) == 1
        assert heros[0].name == "Deadpond"


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
