import pytest
from pydantic.error_wrappers import ValidationError
from sqlmodel import SQLModel


def test_validation_pydantic_v2(clear_sqlmodel):
    """Test validation of implicit and explicit None values.

    # For consistency with pydantic, validators are not to be called on
    # arguments that are not explicitly provided.

    https://github.com/tiangolo/sqlmodel/issues/230
    https://github.com/samuelcolvin/pydantic/issues/1223

    """
    from pydantic import field_validator

    class Hero(SQLModel):
        name: str | None = None
        secret_name: str | None = None
        age: int | None = None

        @field_validator("name", "secret_name", "age")
        def reject_none(cls, v):
            assert v is not None
            return v

    Hero.model_validate({"age": 25})

    with pytest.raises(ValidationError):
        Hero.model_validate({"name": None, "age": 25})


def test_validate_dict_sets_relationship(clear_sqlmodel):
    """A relationship passed inside the dict given to model_validate must be
    set, consistent with the constructor and with model_validate(object)."""

    from sqlmodel import Field, Relationship

    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    team = Team(name="Avengers")

    # constructor already works; model_validate must match it
    assert Hero(name="IronMan", team=team).team is team
    assert Hero.model_validate({"name": "Thor", "team": team}).team is team
    assert Hero.model_validate({"name": "Hulk"}, update={"team": team}).team is team
