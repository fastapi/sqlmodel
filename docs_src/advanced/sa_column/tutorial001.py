from datetime import datetime
from time import sleep
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

    registered_at: datetime = Field(
        sa_column=Column(DateTime(timezone=False), server_default=func.now())
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=False), onupdate=func.now())
    )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    session = Session(engine)

    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)

    session.commit()

    session.close()


def update_hero_age(new_secret_name):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print("Hero:", hero)

        hero.secret_name = new_secret_name
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print("Updated hero:", hero)


def main():
    create_db_and_tables()
    create_heroes()
    sleep(1)
    update_hero_age("Arachnid-Lad")
    sleep(1)
    update_hero_age("The Wallclimber")


if __name__ == "__main__":
    main()
