import random
from typing import Any, Optional

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.ext.mutable import Mutable
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.sql.sqltypes import PydanticJSONType


class Stats(BaseModel, Mutable):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    @classmethod
    def coerce(cls, key: str, value: Any) -> Optional[Any]:
        return value

    def __setattr__(self, key, value):
        # set the attribute
        object.__setattr__(self, key, value)

        # alert all parents to the change
        self.changed()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int]
    stats: Stats = Field(
        default_factory=None,
        sa_column=Column(Stats.as_mutable(PydanticJSONType(type=Stats))),
    )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def random_stat():
    random.seed()

    return Stats(
        strength=random.randrange(1, 20, 2),
        dexterity=random.randrange(1, 20, 2),
        constitution=random.randrange(1, 20, 2),
        intelligence=random.randrange(1, 20, 2),
        wisdom=random.randrange(1, 20, 2),
        charisma=random.randrange(1, 20, 2),
    )


def create_hero():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", stats=random_stat())

    with Session(engine) as session:
        session.add(hero_1)

        session.commit()


def mutate_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero_1 = results.one()

        print("Hero 1:", hero_1.stats)

        hero_1.stats.strength = 100500
        session.commit()

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero_1 = results.one()

        print("Hero 1 strength:", hero_1.stats.strength)

        print("Hero 1:", hero_1)


def main():
    create_db_and_tables()
    create_hero()
    mutate_hero()


if __name__ == "__main__":
    main()
