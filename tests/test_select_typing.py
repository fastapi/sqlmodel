from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool


def test_fields() -> None:
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None
        food: Optional[str] = None

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Hero(name="Deadpond", secret_name="Dive Wilson"))
        session.add(
            Hero(name="Spider-Boy", secret_name="Pedro Parqueador", food="pizza")
        )
        session.add(Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48))

        session.commit()

    # check typing of select with 3 fields
    with Session(engine) as session:
        statement_3 = select(Hero.id, Hero.name, Hero.secret_name)
        results_3 = session.exec(statement_3)
        for hero_3 in results_3:
            assert len(hero_3) == 3
            name_3: str = hero_3[1]
            assert type(name_3) is str
            assert type(hero_3[0]) is int
            assert type(hero_3[2]) is str

    # check typing of select with 4 fields
    with Session(engine) as session:
        statement_4 = select(Hero.id, Hero.name, Hero.secret_name, Hero.age)
        results_4 = session.exec(statement_4)
        for hero_4 in results_4:
            assert len(hero_4) == 4
            name_4: str = hero_4[1]
            assert type(name_4) is str
            assert type(hero_4[0]) is int
            assert type(hero_4[2]) is str
            assert type(hero_4[3]) in [int, type(None)]

    # check typing of select with 5 fields: currently runs but doesn't pass mypy
    # with Session(engine) as session:
    #     statement_5 = select(Hero.id, Hero.name, Hero.secret_name, Hero.age, Hero.food)
    #     results_5 = session.exec(statement_5)
    #     for hero_5 in results_5:
    #         assert len(hero_5) == 5
    #         name_5: str = hero_5[1]
    #         assert type(name_5) is str
    #         assert type(hero_5[0]) is int
    #         assert type(hero_5[2]) is str
    #         assert type(hero_5[3]) in [int, type(None)]
    #         assert type(hero_5[4]) in [str, type(None)]
