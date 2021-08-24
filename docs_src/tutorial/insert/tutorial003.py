from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():  # (1)
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  # (2)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:  # (3)
        session.add(hero_1)  # (4)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()  # (5)
    # (6)


def main():  # (7)
    create_db_and_tables()  # (8)
    create_heroes()  # (9)


if __name__ == "__main__":  # (10)
    main()  # (11)
