from typing import Optional

from sqlalchemy.types import Unicode
from sqlmodel import Field, Session, SQLModel, create_engine


def test_query(clear_sqlmodel):
    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None
        json_data: str = Field(sa_column_kwargs={"type_": Unicode(20)})

    hero_1 = Hero(
        name="Deadpond", secret_name="Dive Wilson", json_data=u"{'parody': 'true 😊'}"
    )

    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

    with Session(engine) as session:
        table = session.query(Hero)._raw_columns[0]
        query_hero = session.query(Hero).first()
        assert query_hero
        assert query_hero.name == hero_1.name
        assert isinstance(table.columns.json_data.type, Unicode)
        assert table.columns.json_data.type._expect_unicode
        assert table.columns.json_data.type.length == len(hero_1.json_data)
