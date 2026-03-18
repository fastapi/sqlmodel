from decimal import Decimal
from typing import Annotated

import pytest
from sqlalchemy import BigInteger, Column, Integer, Numeric, String
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool


def test_sa_column_takes_precedence() -> None:
    class Item(SQLModel, table=True):
        id: int | None = Field(
            default=None,
            sa_column=Column(String, primary_key=True, nullable=False),
        )

    # It would have been nullable with no sa_column
    assert Item.id.nullable is False  # type: ignore
    assert isinstance(Item.id.type, String)  # type: ignore


def test_sa_column_with_annotated_metadata() -> None:
    class Item(SQLModel, table=True):
        id: Annotated[int | None, "meta"] = Field(
            default=None,
            sa_column=Column(String, primary_key=True, nullable=False),
        )

    assert Item.id.nullable is False  # type: ignore
    assert isinstance(Item.id.type, String)  # type: ignore


def test_sa_column_no_sa_args() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column_args=[Integer],
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_sa_kargs() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column_kwargs={"primary_key": True},
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_type() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_type=Integer,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_primary_key() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                primary_key=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_nullable() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                nullable=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_foreign_key() -> None:
    with pytest.raises(RuntimeError):

        class Team(SQLModel, table=True):
            id: int | None = Field(default=None, primary_key=True)
            name: str

        class Hero(SQLModel, table=True):
            id: int | None = Field(default=None, primary_key=True)
            team_id: int | None = Field(
                default=None,
                foreign_key="team.id",
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_unique() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                unique=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_index() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                index=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_ondelete() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column=Column(Integer, primary_key=True),
                ondelete="CASCADE",
            )


def test_sa_type_instance_biginteger() -> None:
    """sa_type accepts TypeEngine instances, not just classes."""

    class Record(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        big_number: int | None = Field(default=None, sa_type=BigInteger())

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Record(big_number=2**40))
        session.commit()

    with Session(engine) as session:
        row = session.exec(select(Record)).first()
        assert row is not None
        assert row.big_number == 2**40


def test_sa_type_instance_numeric() -> None:
    """sa_type accepts parameterised TypeEngine instances like Numeric(...)."""

    class Price(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        amount: Decimal | None = Field(
            default=None, sa_type=Numeric(precision=10, scale=2)
        )

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Price(amount=Decimal("19.99")))
        session.commit()

    with Session(engine) as session:
        row = session.exec(select(Price)).first()
        assert row is not None
        assert row.amount == Decimal("19.99")
