from typing import List, Optional

import pytest
from pydantic.error_wrappers import ValidationError
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.main import Field, Relationship

from .conftest import needs_pydanticv1, needs_pydanticv2


@needs_pydanticv1
def test_validation_pydantic_v1(clear_sqlmodel):
    """Test validation of implicit and explicit None values.

    # For consistency with pydantic, validators are not to be called on
    # arguments that are not explicitly provided.

    https://github.com/tiangolo/sqlmodel/issues/230
    https://github.com/samuelcolvin/pydantic/issues/1223

    """
    from pydantic import validator

    class Hero(SQLModel):
        name: Optional[str] = None
        secret_name: Optional[str] = None
        age: Optional[int] = None

        @validator("name", "secret_name", "age")
        def reject_none(cls, v):
            assert v is not None
            return v

    Hero.validate({"age": 25})

    with pytest.raises(ValidationError):
        Hero.validate({"name": None, "age": 25})


@needs_pydanticv2
def test_validation_pydantic_v2(clear_sqlmodel):
    """Test validation of implicit and explicit None values.

    # For consistency with pydantic, validators are not to be called on
    # arguments that are not explicitly provided.

    https://github.com/tiangolo/sqlmodel/issues/230
    https://github.com/samuelcolvin/pydantic/issues/1223

    """
    from pydantic import field_validator

    class Hero(SQLModel):
        name: Optional[str] = None
        secret_name: Optional[str] = None
        age: Optional[int] = None

        @field_validator("name", "secret_name", "age")
        def reject_none(cls, v):
            assert v is not None
            return v

    Hero.model_validate({"age": 25})

    with pytest.raises(ValidationError):
        Hero.model_validate({"name": None, "age": 25})


@needs_pydanticv1
def test_validation_related_object_not_in_session_pydantic_v1(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    team = Team(name="team")
    hero = Hero(name="hero", team=team)
    with Session(engine) as session:
        session.add(team)
        session.add(hero)
        session.commit()

    with Session(engine) as session:
        hero = session.get(Hero, 1)
        assert session._is_clean()

        new_hero = Hero.validate(hero)

        assert session._is_clean()
        # The new hero is a different instance, but the team is the same
        assert id(new_hero) != id(hero)
        assert id(new_hero.team) == id(hero.team)


@needs_pydanticv2
def test_validation_related_object_not_in_session_pydantic_v2(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        heroes: List["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    team = Team(name="team")
    hero = Hero(name="hero", team=team)
    with Session(engine) as session:
        session.add(team)
        session.add(hero)
        session.commit()

    with Session(engine) as session:
        hero = session.get(Hero, 1)
        assert session._is_clean()

        new_hero = Hero.model_validate(hero)

        assert session._is_clean()
        # The new hero is a different instance, but the team is the same
        assert id(new_hero) != id(hero)
        assert id(new_hero.team) == id(hero.team)
