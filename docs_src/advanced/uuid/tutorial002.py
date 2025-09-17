import uuid
from typing import Union

from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Union[int, None] = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_hero():
    with Session(engine) as session:
        hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
        print("The hero before saving in the DB")
        print(hero_1)
        print("The hero ID was already set")
        print(hero_1.id)
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)
        print("After saving in the DB")
        print(hero_1)


def select_hero():
    with Session(engine) as session:
        hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_2)
        session.commit()
        session.refresh(hero_2)
        hero_id = hero_2.id
        print("Created hero:")
        print(hero_2)
        print("Created hero ID:")
        print(hero_id)

        selected_hero = session.get(Hero, hero_id)
        print("Selected hero:")
        print(selected_hero)
        print("Selected hero ID:")
        print(selected_hero.id)


def main() -> None:
    create_db_and_tables()
    create_hero()
    select_hero()


if __name__ == "__main__":
    main()
