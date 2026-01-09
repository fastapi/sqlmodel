from decimal import Decimal
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    money: Decimal = Field(default=0, max_digits=5, decimal_places=3)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", money=1.1)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", money=0.001)
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, money=2.2)

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

        total_money = hero_1.money + hero_2.money
        print(f"Total money: {total_money}")


def main():
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
