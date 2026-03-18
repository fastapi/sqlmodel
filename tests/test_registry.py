from sqlalchemy.orm import registry

from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_custom_registry_stored_in_model_config(clear_sqlmodel):
    """Test that passing a custom registry via kwargs stores the registry
    (not the table config value) in model_config['registry'].

    This is a regression test for a copy-paste bug where model_config['registry']
    was incorrectly set to the value of config_table instead of config_registry.
    """
    custom_registry = registry()

    class Base(SQLModel, registry=custom_registry):
        pass

    class Hero(Base, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    # The registry stored in model_config should be the custom registry,
    # not a bool (which config_table would be)
    assert Base.model_config.get("registry") is custom_registry
    assert isinstance(Base.model_config.get("registry"), registry)

    # Verify the custom registry is actually functional
    engine = create_engine("sqlite://")
    custom_registry.metadata.create_all(engine)

    with Session(engine) as session:
        hero = Hero(name="Spider-Boy")
        session.add(hero)
        session.commit()
        session.refresh(hero)
        assert hero.id is not None
        assert hero.name == "Spider-Boy"

    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        assert len(heroes) == 1
        assert heroes[0].name == "Spider-Boy"

    custom_registry.dispose()
