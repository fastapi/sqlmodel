import uuid

from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select


def test_annotated_optional_types(database_engine: Engine) -> None:
    from pydantic import UUID4

    class Hero(SQLModel, table=True):
        # Pydantic UUID4 is: Annotated[UUID, UuidVersion(4)]
        id: UUID4 | None = Field(default_factory=uuid.uuid4, primary_key=True)

    engine = database_engine
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        db.commit()
        statement = select(Hero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(hero.id, uuid.UUID)
