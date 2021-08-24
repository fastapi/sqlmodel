from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine


class Weapon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    hero: "Hero" = Relationship(back_populates="weapon")


class Power(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    hero_id: int = Field(foreign_key="hero.id")
    hero: "Hero" = Relationship(back_populates="powers")


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")

    weapon_id: Optional[int] = Field(default=None, foreign_key="weapon.id")
    weapon: Optional[Weapon] = Relationship(back_populates="owner")

    powers: List[Power] = Relationship(back_populates="hero")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
