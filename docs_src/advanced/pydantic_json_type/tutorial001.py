import random
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Stats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int]
    stats: Optional[Stats]


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


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", stats=random_stat())
    hero_2 = Hero(
        name="Spider-Boy", secret_name="Pedro Parqueador", stats=random_stat()
    )
    hero_3 = Hero(
        name="Rusty-Man", secret_name="Tommy Sharp", age=48, stats=random_stat()
    )

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        hero_1 = results.one()
        print("Hero 1:", hero_1)

        statement = select(Hero).where(Hero.name == "Rusty-Man")
        results = session.exec(statement)
        hero_2 = results.one()
        print("Hero 2:", hero_2)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
