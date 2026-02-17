from typing import Optional

import pytest
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel


def test_sa_relationship_no_args() -> None:
    with pytest.raises(RuntimeError):  # pragma: no cover

        class Team(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            headquarters: str

            heroes: list["Hero"] = Relationship(
                back_populates="team",
                sa_relationship_args=["Hero"],
                sa_relationship=relationship("Hero", back_populates="team"),
            )

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            secret_name: str
            age: Optional[int] = Field(default=None, index=True)

            team_id: Optional[int] = Field(default=None, foreign_key="team.id")
            team: Optional[Team] = Relationship(back_populates="heroes")


def test_sa_relationship_no_kwargs() -> None:
    with pytest.raises(RuntimeError):  # pragma: no cover

        class Team(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            headquarters: str

            heroes: list["Hero"] = Relationship(
                back_populates="team",
                sa_relationship_kwargs={"lazy": "selectin"},
                sa_relationship=relationship("Hero", back_populates="team"),
            )

        class Hero(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            name: str = Field(index=True)
            secret_name: str
            age: Optional[int] = Field(default=None, index=True)

            team_id: Optional[int] = Field(default=None, foreign_key="team.id")
            team: Optional[Team] = Relationship(back_populates="heroes")
