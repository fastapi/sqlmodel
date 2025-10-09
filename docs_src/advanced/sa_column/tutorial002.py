import os
from typing import Optional

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Single-column unique via sa_column
    email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    name: str
    secret_name: str
    age: Optional[int] = None

    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint("name", "secret_name", name="uq_hero_name_secret"),
    )


sqlite_file_name = "database_unique.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def create_db_and_tables() -> None:
    # Reset DB for demo
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)
    SQLModel.metadata.create_all(engine)


def create_heroes() -> None:
    with Session(engine) as session:
        hero_1 = Hero(email="ted@richmond.afc", name="Ted Lasso", secret_name="Coach")
        hero_2 = Hero(email="roy@richmond.afc", name="Roy Kent", secret_name="Roy")
        hero_3 = Hero(email="keeley@richmond.afc", name="Keeley Jones", secret_name="Keeley")

        print("Adding Hero 1: Ted Lasso (email=ted@richmond.afc)")
        print("Adding Hero 2: Roy Kent (email=roy@richmond.afc)")
        print("Adding Hero 3: Keeley Jones (email=keeley@richmond.afc)")
        session.add_all([hero_1, hero_2, hero_3])
        session.commit()
        print("Inserted 3 heroes.\n")

        # Duplicate (name, secret_name) should fail (different email)
        hero_4 = Hero(email="roy2@richmond.afc", name="Roy Kent", secret_name="Roy")
        try:
            print("Attempting to insert a duplicate (name, secret_name) ...")
            session.add(hero_4)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print("Composite unique constraint enforced:", str(e.orig))


def select_heroes() -> None:
    with Session(engine) as session:
        print("\nSelecting by email (unique column):")
        statement = select(Hero).where(Hero.email == "ted@richmond.afc")
        hero_1 = session.exec(statement).one()
        print("Hero 1:", hero_1)

        print("\nSelecting by composite key (name, secret_name):")
        statement = select(Hero).where(
            (Hero.name == "Roy Kent") & (Hero.secret_name == "Roy")
        )
        hero_2 = session.exec(statement).one()
        print("Hero 2:", hero_2)


def main() -> None:
    create_db_and_tables()
    create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()
