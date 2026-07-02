from typing import Annotated

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
from sqlmodel import Field, SQLModel


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_takes_precedence(clear_sqlmodel, column_class) -> None:
    class Item(SQLModel, table=True):
        id: int | None = Field(
            default=None,
            sa_column=column_class(String, primary_key=True, nullable=False),
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


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_sa_args(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column_args=[Integer],
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_sa_kargs(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column_kwargs={"primary_key": True},
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_type(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_type=Integer,
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_primary_key(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                primary_key=True,
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_nullable(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                nullable=True,
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_foreign_key(clear_sqlmodel, column_class) -> None:
    with pytest.raises(RuntimeError):

        class Team(SQLModel, table=True):
            id: int | None = Field(default=None, primary_key=True)
            name: str

        class Hero(SQLModel, table=True):
            id: int | None = Field(default=None, primary_key=True)
            team_id: int | None = Field(
                default=None,
                foreign_key="team.id",
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_unique(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                unique=True,
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_index(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                index=True,
                sa_column=column_class(Integer, primary_key=True),
            )


@pytest.mark.parametrize("column_class", [Column, mapped_column])
def test_sa_column_no_ondelete(column_class) -> None:
    with pytest.raises(RuntimeError):

        class Item(SQLModel, table=True):
            id: int | None = Field(
                default=None,
                sa_column=column_class(Integer, primary_key=True),
                ondelete="CASCADE",
            )
