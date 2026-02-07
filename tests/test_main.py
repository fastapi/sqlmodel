from typing import Annotated, Literal, Optional, Union

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_should_allow_duplicate_row_if_unique_constraint_is_not_passed(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        session.add(hero_2)
        session.commit()
        session.refresh(hero_2)

    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        assert len(heroes) == 2
        assert heroes[0].name == heroes[1].name


def test_should_allow_duplicate_row_if_unique_constraint_is_false(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str = Field(unique=False)
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        session.add(hero_2)
        session.commit()
        session.refresh(hero_2)

    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        assert len(heroes) == 2
        assert heroes[0].name == heroes[1].name


def test_should_raise_exception_when_try_to_duplicate_row_if_unique_constraint_is_true(
    clear_sqlmodel,
):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str = Field(unique=True)
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with pytest.raises(IntegrityError):
        with Session(engine) as session:
            session.add(hero_2)
            session.commit()


def test_sa_relationship_property(clear_sqlmodel):
    """Test https://github.com/tiangolo/sqlmodel/issues/315#issuecomment-1272122306"""

    class Team(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(unique=True)
        heroes: list["Hero"] = Relationship(  # noqa: F821
            sa_relationship=RelationshipProperty("Hero", back_populates="team")
        )

    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(unique=True)
        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(
            sa_relationship=RelationshipProperty("Team", back_populates="heroes")
        )

    team_preventers = Team(name="Preventers")
    hero_rusty_man = Hero(name="Rusty-Man", team=team_preventers)

    engine = create_engine("sqlite://", echo=True)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_rusty_man)
        session.commit()
        session.refresh(hero_rusty_man)
        # The next statement should not raise an AttributeError
        assert hero_rusty_man.team
        assert hero_rusty_man.team.name == "Preventers"


def test_composite_primary_key(clear_sqlmodel):
    class UserPermission(SQLModel, table=True):
        user_id: int = Field(primary_key=True)
        resource_id: int = Field(primary_key=True)
        permission: str

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    pk_column_names = {column.name for column in UserPermission.__table__.primary_key}
    assert pk_column_names == {"user_id", "resource_id"}

    with Session(engine) as session:
        perm1 = UserPermission(user_id=1, resource_id=1, permission="read")
        perm2 = UserPermission(user_id=1, resource_id=2, permission="write")
        session.add(perm1)
        session.add(perm2)
        session.commit()

    with pytest.raises(IntegrityError):
        with Session(engine) as session:
            perm3 = UserPermission(user_id=1, resource_id=1, permission="admin")
            session.add(perm3)
            session.commit()


def test_composite_primary_key_and_validator(clear_sqlmodel):
    from pydantic import AfterValidator

    def validate_resource_id(value: int) -> int:
        if value < 1:
            raise ValueError("Resource ID must be positive")
        return value

    class UserPermission(SQLModel, table=True):
        user_id: int = Field(primary_key=True)
        resource_id: Annotated[int, AfterValidator(validate_resource_id)] = Field(
            primary_key=True
        )
        permission: str

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    pk_column_names = {column.name for column in UserPermission.__table__.primary_key}
    assert pk_column_names == {"user_id", "resource_id"}

    with Session(engine) as session:
        perm1 = UserPermission(user_id=1, resource_id=1, permission="read")
        perm2 = UserPermission(user_id=1, resource_id=2, permission="write")
        session.add(perm1)
        session.add(perm2)
        session.commit()

    with pytest.raises(IntegrityError):
        with Session(engine) as session:
            perm3 = UserPermission(user_id=1, resource_id=1, permission="admin")
            session.add(perm3)
            session.commit()


def test_foreign_key_ondelete_with_annotated(clear_sqlmodel):
    from pydantic import AfterValidator

    def ensure_positive(value: int) -> int:
        if value < 0:
            raise ValueError("Team ID must be positive")
        return value

    class Team(SQLModel, table=True):
        id: int = Field(primary_key=True)
        name: str

    class Hero(SQLModel, table=True):
        id: int = Field(primary_key=True)
        team_id: Annotated[int, AfterValidator(ensure_positive)] = Field(
            foreign_key="team.id",
            ondelete="CASCADE",
        )
        name: str

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    team_id_column = Hero.__table__.c.team_id  # type: ignore[attr-defined]
    foreign_keys = list(team_id_column.foreign_keys)
    assert len(foreign_keys) == 1
    assert foreign_keys[0].ondelete == "CASCADE"
    assert team_id_column.nullable is False


def test_literal_valid_values(clear_sqlmodel, caplog):
    """Test https://github.com/fastapi/sqlmodel/issues/57"""

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        all_str: Literal["a", "b", "c"]
        mixed: Literal["yes", "no", 1, 0]
        all_int: Literal[1, 2, 3]
        int_bool: Literal[0, 1, True, False]
        all_bool: Literal[True, False]

    obj = Model(
        all_str="a",
        mixed="yes",
        all_int=1,
        int_bool=True,
        all_bool=False,
    )

    engine = create_engine("sqlite://", echo=True)

    SQLModel.metadata.create_all(engine)

    # Check DDL
    assert "all_str VARCHAR NOT NULL" in caplog.text
    assert "mixed VARCHAR NOT NULL" in caplog.text
    assert "all_int INTEGER NOT NULL" in caplog.text
    assert "int_bool INTEGER NOT NULL" in caplog.text
    assert "all_bool BOOLEAN NOT NULL" in caplog.text

    # Check query
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        assert isinstance(obj.all_str, str)
        assert obj.all_str == "a"
        assert isinstance(obj.mixed, str)
        assert obj.mixed == "yes"
        assert isinstance(obj.all_int, int)
        assert obj.all_int == 1
        assert isinstance(obj.int_bool, int)
        assert obj.int_bool == 1
        assert isinstance(obj.all_bool, bool)
        assert obj.all_bool is False


def test_literal_constraints_invalid_values(clear_sqlmodel):
    """DB should reject values that are not part of the Literal choices."""

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        all_str: Literal["a", "b", "c"]
        mixed: Literal["yes", "no", 1, 0]
        all_int: Literal[1, 2, 3]
        int_bool: Literal[0, 1, True, False]
        all_bool: Literal[True, False]

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    # Helper to attempt a raw insert that bypasses Pydantic validation so we
    # can verify that the database-level CHECK constraints are enforced.
    def insert_raw(values: dict[str, object]) -> None:
        stmt = text(
            "INSERT INTO model (all_str, mixed, all_int, int_bool, all_bool) "
            "VALUES (:all_str, :mixed, :all_int, :int_bool, :all_bool)"
        ).bindparams(**values)
        with pytest.raises(IntegrityError):
            with Session(engine) as session:
                session.exec(stmt)
                session.commit()

    # Invalid string literal for all_str
    insert_raw(
        {
            "all_str": "z",  # invalid, not in {"a","b","c"}
            "mixed": "yes",
            "all_int": 1,
            "int_bool": 1,
            "all_bool": 0,
        }
    )

    # Invalid int literal for all_int
    insert_raw(
        {
            "all_str": "a",
            "mixed": "yes",
            "all_int": 5,  # invalid, not in {1,2,3}
            "int_bool": 1,
            "all_bool": 0,
        }
    )

    # Invalid bool literal for all_bool
    insert_raw(
        {
            "all_str": "a",
            "mixed": "yes",
            "all_int": 1,
            "int_bool": 1,
            "all_bool": 2,  # invalid boolean value
        }
    )


def test_literal_optional_and_union_constraints(clear_sqlmodel):
    """Literals inside Optional/Union should also be enforced at the DB level."""

    class Model(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        opt_str: Optional[Literal["x", "y"]] = None
        union_int: Union[Literal[10, 20], None] = None

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    # Valid values should be accepted
    obj = Model(opt_str="x", union_int=10)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        assert obj.opt_str == "x"
        assert obj.union_int == 10

    # Invalid values should be rejected by the database
    def insert_raw(values: dict[str, object]) -> None:
        stmt = text(
            "INSERT INTO model (opt_str, union_int) VALUES (:opt_str, :union_int)"
        ).bindparams(**values)
        with pytest.raises(IntegrityError):
            with Session(engine) as session:
                session.exec(stmt)
                session.commit()

    # opt_str not in {"x", "y"}
    insert_raw({"opt_str": "z", "union_int": 10})

    # union_int not in {10, 20}
    insert_raw({"opt_str": "x", "union_int": 30})
