from datetime import datetime

from sqlmodel import (
    Field,
    SoftDeleteMixin,
    SoftDeleteSession,
    SQLModel,
    create_engine,
    select,
)


def test_soft_delete_filters_select_results() -> None:
    class Hero(SQLModel, SoftDeleteMixin, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with SoftDeleteSession(engine) as session:
        active_hero = Hero(name="Deadpond")
        deleted_hero = Hero(name="Spider-Boy")
        session.add(active_hero)
        session.add(deleted_hero)
        session.commit()

        session.delete(deleted_hero)
        session.commit()

        heroes = session.exec(select(Hero)).all()
        assert heroes == [active_hero]
        assert isinstance(deleted_hero.deleted_at, datetime)


def test_soft_delete_can_include_deleted_results() -> None:
    class Hero(SQLModel, SoftDeleteMixin, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with SoftDeleteSession(engine) as session:
        active_hero = Hero(name="Deadpond")
        deleted_hero = Hero(name="Spider-Boy")
        session.add(active_hero)
        session.add(deleted_hero)
        session.commit()

        session.delete(deleted_hero)
        session.commit()

        statement = select(Hero).execution_options(include_deleted=True)
        heroes = session.exec(statement).all()
        assert heroes == [active_hero, deleted_hero]


def test_soft_delete_supports_custom_field_name() -> None:
    class Hero(SQLModel, table=True):
        __soft_delete_field__ = "removed_at"

        id: int | None = Field(default=None, primary_key=True)
        name: str
        removed_at: datetime | None = Field(default=None)

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with SoftDeleteSession(engine) as session:
        active_hero = Hero(name="Deadpond")
        deleted_hero = Hero(name="Spider-Boy")
        session.add(active_hero)
        session.add(deleted_hero)
        session.commit()

        session.delete(deleted_hero)
        session.commit()

        heroes = session.exec(select(Hero)).all()
        assert heroes == [active_hero]
        assert isinstance(deleted_hero.removed_at, datetime)
