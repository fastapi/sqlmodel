from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, create_model


def test_create_model(clear_sqlmodel):
    """
    Test dynamic model creation, query, and deletion
    """

    hero = create_model(
        "Hero",
        {
            "id": (Optional[int], Field(default=None, primary_key=True)),
            "name": str,
            "secret_name": (str,),  # test 1-tuple
            "age": (Optional[int], None),
        },
        table=True,
    )

    hero_1 = hero(**{"name": "Deadpond", "secret_name": "Dive Wilson"})

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        query_hero = session.query(hero).first()
        assert query_hero
        assert query_hero.id == hero_1.id
        assert query_hero.name == hero_1.name
        assert query_hero.secret_name == hero_1.secret_name
        assert query_hero.age == hero_1.age

    with Session(engine) as session:
        session.delete(hero_1)
        session.commit()

    with Session(engine) as session:
        query_hero = session.query(hero).first()
        assert not query_hero
