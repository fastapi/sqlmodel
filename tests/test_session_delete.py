import pytest
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, create_engine, Field
from sqlmodel.main import default_registry
from sqlmodel.soft_delete import SoftDeleteMixin
from sqlmodel.soft_delete_session import SoftDeleteSession


@pytest.fixture(autouse=True)
def clear_sqlmodel():
    # Local override to avoid global dispose
    pass


def test_soft_delete():
    # Define model inside test to avoid registry conflicts
    class SoftDeleteHero(SQLModel, SoftDeleteMixin, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with SoftDeleteSession(engine) as session:
        hero = SoftDeleteHero(name="Test Hero")
        session.add(hero)
        session.commit()

        # Soft delete
        session.delete(hero)
        session.commit()

        # Check soft deleted
        assert hero.deleted_at is not None
        assert isinstance(hero.deleted_at, datetime)

        # Refresh to confirm
        session.refresh(hero)
        assert hero.deleted_at is not None


def test_hard_delete():
    # Define model inside test to avoid registry conflicts
    class HardDeleteHero(SQLModel, SoftDeleteMixin, table=True):
        __tablename__ = "hard_delete_heroes"
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with SoftDeleteSession(engine) as session:
        hero = HardDeleteHero(name="Test Hero")
        session.add(hero)
        session.commit()

        # Hard delete
        session.delete(hero, hard_delete=True)
        session.commit()

        # Check hard deleted (would raise if not handled, but since hard delete, it's gone)
        # In SQLAlchemy, after hard delete, the object is detached
        assert hero.id is None or session.get(HardDeleteHero, hero.id) is None