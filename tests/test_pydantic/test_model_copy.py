import pytest
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def test_model_copy_non_table(clear_sqlmodel):
    class Item(SQLModel):
        name: str
        value: int

    item = Item(name="Test Item", value=42)
    copied = item.model_copy()
    assert copied.name == "Test Item"
    assert copied.value == 42
    assert copied is not item

    updated_copy = item.model_copy(update={"name": "New Name"})
    assert updated_copy.name == "New Name"
    assert updated_copy.value == 42


def test_model_copy_unpersisted_table(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str

    hero = Hero(name="Deadpond", secret_name="Dive Wilson")
    copied = hero.model_copy()
    assert copied.name == "Deadpond"
    assert copied.secret_name == "Dive Wilson"
    assert copied.id is None
    assert copied is not hero
    assert copied._sa_instance_state is not hero._sa_instance_state
    assert copied._sa_instance_state.obj() is copied


def test_model_copy_persisted_table(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: int | None = None

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        hero = Hero(name="Deadpond", secret_name="Dive Wilson", age=30)
        session.add(hero)
        session.commit()
        session.refresh(hero)

        # Create copy of persisted instance
        hero_copy = hero.model_copy(update={"name": "Spider-Boy"}, deep=True)

        assert hero_copy is not hero
        assert hero_copy._sa_instance_state is not hero._sa_instance_state
        assert hero_copy._sa_instance_state.obj() is hero_copy
        assert hero_copy.name == "Spider-Boy"
        assert hero_copy.secret_name == "Dive Wilson"
        assert hero_copy.age == 30

        # Verify mutating the copy does not alter the original in session
        hero_copy.secret_name = "Peter Parker"
        assert hero.secret_name == "Dive Wilson"

        # Verify copy can be persisted independently
        hero_copy.id = None
        session.add(hero_copy)
        session.commit()
        session.refresh(hero_copy)

        assert hero.id == 1
        assert hero.name == "Deadpond"
        assert hero_copy.id == 2
        assert hero_copy.name == "Spider-Boy"

    with Session(engine) as session:
        all_heroes = session.exec(select(Hero)).all()
        assert len(all_heroes) == 2
        assert {h.name for h in all_heroes} == {"Deadpond", "Spider-Boy"}


def test_model_copy_with_relationships(clear_sqlmodel):
    class Team(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        heroes: list["Hero"] = Relationship(back_populates="team")

    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        team_id: int | None = Field(default=None, foreign_key="team.id")
        team: Team | None = Relationship(back_populates="heroes")

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        team = Team(name="Avengers")
        hero = Hero(name="Deadpond", team=team)
        session.add(team)
        session.add(hero)
        session.commit()
        session.refresh(hero)

        hero_copy = hero.model_copy(update={"name": "Rusty-Man"})
        assert hero_copy._sa_instance_state is not hero._sa_instance_state
        assert hero_copy._sa_instance_state.obj() is hero_copy
        assert hero_copy.name == "Rusty-Man"


def test_deprecated_copy(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    hero = Hero(name="Deadpond")
    with pytest.deprecated_call():
        hero_copy = hero.copy(update={"name": "Spider-Boy"})
    assert hero_copy.name == "Spider-Boy"
    assert hero_copy._sa_instance_state is not hero._sa_instance_state
    assert hero_copy._sa_instance_state.obj() is hero_copy
