from sqlalchemy import Engine
from sqlalchemy.engine import ScalarResult, TupleResult
from sqlalchemy.sql.elements import UnaryExpression
from sqlmodel import (
    Field,
    Session,
    SQLModel,
    asc,
    col,
    desc,
    nulls_first,
    nulls_last,
    select,
)
from typing_extensions import assert_type


def test_fields(database_engine: Engine) -> None:
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: int | None = None
        food: str | None = None

    engine = database_engine

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
        statement_3 = select(col(Hero.id), Hero.name, Hero.secret_name)
        results_3 = session.exec(statement_3)
        assert_type(results_3, TupleResult[tuple[int | None, str, str]])
        for hero_3 in results_3:
            assert len(hero_3) == 3
            name_3: str = hero_3[1]
            assert type(name_3) is str
            assert type(hero_3[0]) is int
            assert type(hero_3[2]) is str

    # check typing of select with 4 fields
    with Session(engine) as session:
        statement_4 = select(col(Hero.id), Hero.name, Hero.secret_name, col(Hero.age))
        results_4 = session.exec(statement_4)
        assert_type(results_4, TupleResult[tuple[int | None, str, str, int | None]])
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


def test_scalar_results(database_engine: Engine) -> None:
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    SQLModel.metadata.create_all(database_engine)
    with Session(database_engine) as session:
        session.add(Hero(name="Deadpond"))
        session.commit()

        statement = select(Hero)
        result = session.exec(statement)
        assert_type(result, ScalarResult[Hero])
        assert result.one().name == "Deadpond"

        scalars = session.scalars(statement)
        assert_type(scalars, ScalarResult[Hero])
        assert scalars.one().name == "Deadpond"

        scalar_subquery = (
            select(Hero.name)
            .where(Hero.name == "Deadpond")
            .group_by(Hero.name)
            .having(Hero.name == "Deadpond")
            .scalar_subquery()
        )
        name = session.exec(select(scalar_subquery)).one()
        assert_type(name, str)
        assert name == "Deadpond"


def test_ordering_types() -> None:
    class Hero(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str

    ascending = asc(Hero.id)
    assert_type(ascending, UnaryExpression[int])
    assert str(ascending) == "hero.id ASC"

    descending = desc(Hero.id)
    assert_type(descending, UnaryExpression[int])
    assert str(descending) == "hero.id DESC"

    first = nulls_first(Hero.name)
    assert_type(first, UnaryExpression[str])
    assert str(first) == "hero.name NULLS FIRST"

    last = nulls_last(Hero.name)
    assert_type(last, UnaryExpression[str])
    assert str(last) == "hero.name NULLS LAST"
