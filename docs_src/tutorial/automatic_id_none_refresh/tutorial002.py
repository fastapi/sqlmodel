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


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  # (1)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")  # (2)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)  # (3)

    print("Before interacting with the database")  # (4)
    print("Hero 1:", hero_1)  # (5)
    print("Hero 2:", hero_2)  # (6)
    print("Hero 3:", hero_3)  # (7)

    with Session(engine) as session:  # (8)
        session.add(hero_1)  # (9)
        session.add(hero_2)  # (10)
        session.add(hero_3)  # (11)

        print("After adding to the session")  # (12)
        print("Hero 1:", hero_1)  # (13)
        print("Hero 2:", hero_2)  # (14)
        print("Hero 3:", hero_3)  # (15)

        session.commit()  # (16)

        print("After committing the session")  # (17)
        print("Hero 1:", hero_1)  # (18)
        print("Hero 2:", hero_2)  # (19)
        print("Hero 3:", hero_3)  # (20)

        print("After committing the session, show IDs")  # (21)
        print("Hero 1 ID:", hero_1.id)  # (22)
        print("Hero 2 ID:", hero_2.id)  # (23)
        print("Hero 3 ID:", hero_3.id)  # (24)

        print("After committing the session, show names")  # (25)
        print("Hero 1 name:", hero_1.name)  # (26)
        print("Hero 2 name:", hero_2.name)  # (27)
        print("Hero 3 name:", hero_3.name)  # (28)

        session.refresh(hero_1)  # (29)
        session.refresh(hero_2)  # (30)
        session.refresh(hero_3)  # (31)

        print("After refreshing the heroes")  # (32)
        print("Hero 1:", hero_1)  # (33)
        print("Hero 2:", hero_2)  # (34)
        print("Hero 3:", hero_3)  # (35)
    # (36)

    print("After the session closes")  # (37)
    print("Hero 1:", hero_1)  # (38)
    print("Hero 2:", hero_2)  # (39)
    print("Hero 3:", hero_3)  # (40)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
