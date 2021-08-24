from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select  # (1)


class Hero(SQLModel, table=True):  # (2)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)  # (3)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # (4)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  # (5)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:  # (6)
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()


def select_heroes():
    with Session(engine) as session:  # (7)
        statement = select(Hero)  # (8)
        results = session.exec(statement)  # (9)
        for hero in results:  # (10)
            print(hero)  # (11)
    # (12)


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()  # (13)


if __name__ == "__main__":
    main()
