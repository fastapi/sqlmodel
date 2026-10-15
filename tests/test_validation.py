import pytest
from pydantic.error_wrappers import ValidationError
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


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


def test_table_model_field_validator(clear_sqlmodel):
    from pydantic import field_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

        @field_validator("name")
        @classmethod
        def name_must_not_be_empty(cls, v: str) -> str:
            if not v.strip():
                raise ValueError("name must not be empty")
            return v

    Hero(name="Deadpond", age=25)

    with pytest.raises(ValidationError):
        Hero(name="", age=25)


def test_table_model_field_validator_before_mode(clear_sqlmodel):
    from pydantic import field_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

        @field_validator("name", mode="before")
        @classmethod
        def coerce_name(cls, v: object) -> str:
            if isinstance(v, int):
                return f"Hero-{v}"
            return v

    hero = Hero(name=42)
    assert hero.name == "Hero-42"


def test_table_model_model_validator_after(clear_sqlmodel):
    from pydantic import model_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str

        @model_validator(mode="after")
        def names_must_differ(self) -> "Hero":
            if self.name == self.secret_name:
                raise ValueError("name and secret_name must differ")
            return self

    Hero(name="Deadpond", secret_name="Dive Wilson")

    with pytest.raises(ValidationError):
        Hero(name="Same", secret_name="Same")


def test_table_model_model_validator_before(clear_sqlmodel):
    from pydantic import model_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

        @model_validator(mode="before")
        @classmethod
        def uppercase_name(cls, data: dict) -> dict:
            if "name" in data:
                data["name"] = data["name"].upper()
            return data

    hero = Hero(name="deadpond")
    assert hero.name == "DEADPOND"


def test_table_model_before_validator_annotated(clear_sqlmodel):
    from typing import Annotated

    from pydantic import BeforeValidator

    def parse_int(v: object) -> object:
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: Annotated[int | None, BeforeValidator(parse_int)] = None

    hero = Hero(name="Deadpond", age="25")
    assert hero.age == 25


def test_table_model_orm_round_trip_with_validator(clear_sqlmodel):
    from pydantic import field_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

        @field_validator("age")
        @classmethod
        def double_age(cls, v: int | None) -> int | None:
            if v is not None:
                return v * 2
            return v

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    hero = Hero(name="Deadpond", age=25)
    assert hero.age == 50

    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)

    with Session(engine) as session:
        loaded = session.exec(select(Hero)).first()
        assert loaded is not None
        assert loaded.name == "Deadpond"
        assert loaded.age == 50

    SQLModel.metadata.clear()


def test_validation_does_not_run_on_orm_load(clear_sqlmodel):
    from pydantic import field_validator

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

        @field_validator("name")
        @classmethod
        def name_must_be_short(cls, v: str) -> str:
            if len(v) > 5:
                raise ValueError("too long")
            return v

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Hero(name="short"))
        session.commit()

    with engine.connect() as conn:
        conn.execute(
            Hero.__table__.update()
            .where(Hero.__table__.c.id == 1)
            .values(name="this is way too long")
        )
        conn.commit()

    with Session(engine) as session:
        loaded = session.exec(select(Hero)).first()
        assert loaded is not None
        assert loaded.name == "this is way too long"

    SQLModel.metadata.clear()


def test_table_model_relationship_without_related_object(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    team = Team(name="Preventers")
    hero = Hero(name="Deadpond")

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(team)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.team is None

    SQLModel.metadata.clear()


def test_table_model_relationship_assigned_after_construction(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    team = Team(name="Preventers")
    hero = Hero(name="Deadpond")
    hero.team = team

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.team is not None
        assert hero.team.name == "Preventers"

    SQLModel.metadata.clear()


def test_table_model_model_validate_still_works(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        age: int | None = None

    hero = Hero.model_validate({"name": "Deadpond", "age": 25})
    assert hero.name == "Deadpond"
    assert hero.age == 25

    with pytest.raises(ValidationError):
        Hero.model_validate({"name": "Deadpond", "age": "not a number"})
