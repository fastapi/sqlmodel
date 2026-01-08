import uuid
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


def test_annotated_optional_types(clear_sqlmodel) -> None:
    from pydantic import UUID4

    class Hero(SQLModel, table=True):
        # Pydantic UUID4 is: Annotated[UUID, UuidVersion(4)]
        id: Optional[UUID4] = Field(default_factory=uuid.uuid4, primary_key=True)

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        hero = Hero()
        db.add(hero)
        db.commit()
        statement = select(Hero)
        result = db.exec(statement).all()
    assert len(result) == 1
    assert isinstance(hero.id, uuid.UUID)
