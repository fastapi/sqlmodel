from typing import Any, Union

import pytest
from sqlmodel import Field, Relationship, SQLModel


def test_ondelete_requires_nullable(clear_sqlmodel: Any) -> None:
    with pytest.raises(RuntimeError) as exc:

        class Team(SQLModel, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)

            heroes: list["Hero"] = Relationship(
                back_populates="team", passive_deletes="all"
            )

        class Hero(SQLModel, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            secret_name: str
            age: Union[int, None] = Field(default=None, index=True)

            team_id: int = Field(foreign_key="team.id", ondelete="SET NULL")
            team: Team = Relationship(back_populates="heroes")

    assert 'ondelete="SET NULL" requires nullable=True' in str(exc.value)


def test_ondelete_requires_foreign_key(clear_sqlmodel: Any) -> None:
    with pytest.raises(RuntimeError) as exc:

        class Team(SQLModel, table=True):
            id: Union[int, None] = Field(default=None, primary_key=True)

            age: int = Field(ondelete="CASCADE")

    assert "ondelete can only be used with foreign_key" in str(exc.value)
