from typing import Any

import pytest
from sqlalchemy import ForeignKey, Integer, String
from sqlmodel import Field, SQLModel, create_engine


def test_sa_column_args(clear_sqlmodel, caplog) -> None:
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        team_id: int | None = Field(
            default=None,
            sa_column_args=[ForeignKey("team.id")],
        )

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)
    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE hero" in message
    ][0]
    assert "FOREIGN KEY(team_id) REFERENCES team (id)" in create_table_log


def test_sa_column_kargs(clear_sqlmodel, caplog) -> None:
    class Item(SQLModel, table=True):
        id: int | None = Field(
            default=None,
            sa_column_kwargs={"primary_key": True},
        )

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)
    create_table_log = [
        message for message in caplog.messages if "CREATE TABLE item" in message
    ][0]
    assert "PRIMARY KEY (id)" in create_table_log


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
