from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from sqlalchemy import Engine, event, insert, inspect
from sqlmodel import Field, Relationship, Session, SQLModel


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


@pytest.mark.parametrize("expired", [False, True], ids=["loaded", "expired"])
def test_frozen_field_assignment_preserves_pending_edits(
    database_engine: Engine, expired: bool
) -> None:
    class Hero(SQLModel, table=True):
        id: int = Field(primary_key=True)
        code: str = Field(schema_extra={"frozen": True})
        name: str

    SQLModel.metadata.create_all(database_engine)
    with database_engine.begin() as connection:
        connection.execute(insert(Hero).values(id=1, code="original", name="old"))

    on_set = Mock()
    event.listen(Hero.code, "set", on_set, active_history=True)
    with Session(database_engine) as session:
        hero = session.get(Hero, 1)
        assert hero is not None
        hero.name = "updated"
        if expired:
            session.expire(hero, ["code"])

        with pytest.raises(ValidationError) as exc_info:
            hero.code = "rejected"

        (error,) = exc_info.value.errors()
        assert error["type"] == "frozen_field"
        assert error["loc"] == ("code",)
        assert error["input"] == "rejected"
        state = inspect(hero)
        if expired:
            assert "code" in state.expired_attributes
        assert not state.attrs.code.history.has_changes()
        assert hero.code == "original"
        session.commit()

    on_set.assert_not_called()
    with Session(database_engine) as session:
        saved = session.get(Hero, 1)
        assert saved is not None
        assert (saved.code, saved.name) == ("original", "updated")


@pytest.mark.parametrize(
    "field_frozen", [False, True], ids=["model", "model-and-field"]
)
def test_frozen_model_assignment_preserves_primary_key(
    database_engine: Engine, field_frozen: bool
) -> None:
    class Hero(SQLModel, table=True):
        model_config = {"frozen": True}
        id: int = Field(primary_key=True, schema_extra={"frozen": field_frozen})

    SQLModel.metadata.create_all(database_engine)
    with database_engine.begin() as connection:
        connection.execute(insert(Hero).values(id=1))

    with Session(database_engine) as session:
        hero = session.get(Hero, 1)
        assert hero is not None
        with pytest.raises(ValidationError) as exc_info:
            hero.id = 2

        (error,) = exc_info.value.errors()
        assert error["type"] == "frozen_instance"
        assert error["loc"] == ("id",)
        session.commit()

    with Session(database_engine) as session:
        assert session.get(Hero, 1) is not None
        assert session.get(Hero, 2) is None


def test_frozen_foreign_key_preserves_pending_relationship_change(
    database_engine: Engine,
) -> None:
    class Team(SQLModel, table=True):
        id: int = Field(primary_key=True)

    class Hero(SQLModel, table=True):
        id: int = Field(primary_key=True)
        team_id: int = Field(foreign_key="team.id", schema_extra={"frozen": True})
        team: Team = Relationship()

    SQLModel.metadata.create_all(database_engine)
    with database_engine.begin() as connection:
        connection.execute(insert(Team), [{"id": 1}, {"id": 2}])
        connection.execute(insert(Hero).values(id=1, team_id=1))

    with Session(database_engine) as session:
        hero = session.get(Hero, 1)
        team = session.get(Team, 2)
        assert hero is not None
        assert team is not None
        hero.team = team
        with pytest.raises(ValidationError):
            hero.team_id = 3

        assert hero.team_id == 1
        session.commit()

    with Session(database_engine) as session:
        saved = session.get(Hero, 1)
        assert saved is not None
        assert saved.team_id == 2
