from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select


def test_created_and_instantiated_from_db_instances_are_equal(clear_sqlmodel):
    class User(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        username: str
        email: str = "test@test.com"
        last_updated: datetime = Field(default_factory=datetime.now)

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    user_1 = User(username="test_user")
    user_2 = User(username="test_user_2")

    assert user_1 != user_2

    with Session(engine) as session:
        session.add(user_1)
        session.add(user_2)
        session.commit()

        session.refresh(user_1)
        session.refresh(user_2)

        assert user_1 != user_2

    with Session(engine) as session:
        session.merge(user_1)
        session.merge(user_2)

        instantiated_user_1 = session.exec(
            select(User).where(User.username == user_1.username)
        ).one()

        instantiated_user_2 = session.exec(
            select(User).where(User.username == user_2.username)
        ).one()

        assert user_1 != user_2
        assert user_1 == instantiated_user_1
        assert user_2 == instantiated_user_2
