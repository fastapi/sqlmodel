from typing import Optional

import pytest
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, SQLModel


def test_sa_column_takes_precedence() -> None:
    class Item(SQLModel, table=True):
        id: Optional[int] = Field(
            default=None,
            sa_column=Column(String, primary_key=True, nullable=False),
        )

    # It would have been nullable with no sa_column
    assert Item.id.nullable is False  # type: ignore
    assert isinstance(Item.id.type, String)  # type: ignore


def test_sa_column_no_sa_args() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                sa_column_args=[Integer],
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_sa_kargs() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                sa_column_kwargs={"primary_key": True},
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_type() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                sa_type=Integer,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_primary_key() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                primary_key=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_nullable() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                nullable=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_foreign_key() -> None:
    with pytest.raises(RuntimeError):

        class Team(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            team_id: Optional[int] = Field(
                default=None,
                foreign_key="team.id",
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_unique() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                unique=True,
                sa_column=Column(Integer, primary_key=True),
            )


def test_sa_column_no_index() -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: Optional[int] = Field(
                default=None,
                index=True,
                sa_column=Column(Integer, primary_key=True),
            )
