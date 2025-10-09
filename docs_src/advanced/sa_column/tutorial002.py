from typing import Optional

from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Single-column unique using sa_column for full control (e.g., explicit SQL type and nullability)
    email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    name: str
    secret_name: str
    age: Optional[int] = None

    # Composite (multi-column) unique constraint using the idiomatic SQLAlchemy approach
    __table_args__ = (
        UniqueConstraint("name", "secret_name", name="uq_hero_name_secret"),
    )


sqlite_file_name = "database_unique.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def create_heroes() -> None:
    hero_1 = Hero(email="ted@richmond.afc", name="Ted Lasso", secret_name="Coach")
    hero_2 = Hero(email="roy@richmond.afc", name="Roy Kent", secret_name="Roy")
    hero_3 = Hero(
        email="keeley@richmond.afc", name="Keeley Jones", secret_name="Keeley"
    )

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()


def select_heroes() -> None:
    with Session(engine) as session:
        statement = select(Hero).where(Hero.email == "ted@richmond.afc")
        hero_1 = session.exec(statement).one()
        print("Hero 1:", hero_1)

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
