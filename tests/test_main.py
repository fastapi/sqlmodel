from typing import Annotated, Optional

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from .conftest import needs_pydanticv2


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

    insp: Inspector = inspect(engine)
    pk_constraint = insp.get_pk_constraint(str(UserPermission.__tablename__))

    assert len(pk_constraint["constrained_columns"]) == 2
    assert "user_id" in pk_constraint["constrained_columns"]
    assert "resource_id" in pk_constraint["constrained_columns"]

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


@needs_pydanticv2
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

    insp: Inspector = inspect(engine)
    pk_constraint = insp.get_pk_constraint(str(UserPermission.__tablename__))

    assert len(pk_constraint["constrained_columns"]) == 2
    assert "user_id" in pk_constraint["constrained_columns"]
    assert "resource_id" in pk_constraint["constrained_columns"]

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
