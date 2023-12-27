from typing import Optional

from sqlalchemy import Text
from sqlmodel import Field, Session, SQLModel, create_engine, select
from wonderwords import RandomWord


class Villian(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    country_code: str = Field(max_length=2)
    backstory: str = Field(sa_type=Text())


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def generate_backstory(words: int) -> str:
    return " ".join(RandomWord().random_words(words, regex=r"\S+"))


def create_villains():
    villian_1 = Villian(
        name="Green Gobbler", country_code="US", backstory=generate_backstory(500)
    )
    villian_2 = Villian(
        name="Arnim Zozza", country_code="DE", backstory=generate_backstory(500)
    )
    villian_3 = Villian(
        name="Low-key", country_code="AS", backstory=generate_backstory(500)
    )

    with Session(engine) as session:
        session.add(villian_1)
        session.add(villian_2)
        session.add(villian_3)

        session.commit()


def count_words(sentence: str) -> int:
    return sentence.count(" ") + 1


def select_villians():
    with Session(engine) as session:
        statement = select(Villian).where(Villian.name == "Green Gobbler")
        results = session.exec(statement)
        villian_1 = results.one()
        print(
            "Villian 1:",
            {"name": villian_1.name, "country_code": villian_1.country_code},
            count_words(villian_1.backstory),
        )

        statement = select(Villian).where(Villian.name == "Low-key")
        results = session.exec(statement)
        villian_2 = results.one()
        print(
            "Villian 2:",
            {"name": villian_2.name, "country_code": villian_2.country_code},
            count_words(villian_1.backstory),
        )


def main():
    create_db_and_tables()
    create_villains()
    select_villians()


if __name__ == "__main__":
    main()
