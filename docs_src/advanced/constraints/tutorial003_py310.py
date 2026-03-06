from sqlalchemy import CheckConstraint
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    __table_args__ = (CheckConstraint("age >= 0", name="age_non_negative"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Spider-Boy", age=16, secret_name="Pedro Parqueador")
    hero_2 = Hero(name="Baby Hero", age=0, secret_name="Little One")

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)

        print("Created hero:", hero_1)
        print("Created hero:", hero_2)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
