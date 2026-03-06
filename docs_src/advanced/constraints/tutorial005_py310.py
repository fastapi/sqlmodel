from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    age: int
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", age=48, secret_name="Dive Wilson")

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)
        print("✅ Created hero:", hero_1)

        # Now try to create another hero with the same name
        duplicate_hero = Hero(name="Deadpond", age=25, secret_name="Wade Wilson")
        session.add(duplicate_hero)
        
        try:
            session.commit()
            print("❌ This shouldn't happen - duplicate was allowed!")
        except IntegrityError as e:
            session.rollback()
            print("🚫 Constraint violation caught:")
            print(f"   Error: {e}")


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
