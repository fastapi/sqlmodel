from typing import Any

import pytest
from sqlalchemy import Engine, ForeignKey, Integer, String, inspect
from sqlmodel import Field, SQLModel


def test_sa_column_args(database_engine: Engine) -> None:
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        team_id: int | None = Field(
            default=None,
            sa_column_args=[ForeignKey("team.id")],
        )

    engine = database_engine
    SQLModel.metadata.create_all(engine)
    foreign_keys = inspect(engine).get_foreign_keys("hero")
    assert len(foreign_keys) == 1
    assert foreign_keys[0]["constrained_columns"] == ["team_id"]
    assert foreign_keys[0]["referred_table"] == "team"
    assert foreign_keys[0]["referred_columns"] == ["id"]


def test_sa_column_kargs(database_engine: Engine) -> None:
    class Item(SQLModel, table=True):
        id: int | None = Field(
            default=None,
            sa_column_kwargs={"primary_key": True},
        )

    engine = database_engine
    SQLModel.metadata.create_all(engine)
    primary_key = inspect(engine).get_pk_constraint("item")
    assert primary_key["constrained_columns"] == ["id"]


@pytest.mark.parametrize(
    "field_kwargs",
    [
        {"sa_column_kwargs": {"type_": Integer}},
        {"sa_type": String, "sa_column_kwargs": {"type_": Integer}},
    ],
)
def test_sa_column_kwargs_type_raises(field_kwargs: dict[str, Any]) -> None:
    with pytest.raises(
        RuntimeError,
        match="Passing type_ is not supported in sa_column_kwargs, use sa_type instead",
    ):
        Field(**field_kwargs)
