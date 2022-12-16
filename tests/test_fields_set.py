from datetime import datetime, timedelta

from sqlmodel import Field, SQLModel


def test_fields_set():
    class User(SQLModel):
        username: str
        email: str = "test@test.com"
        last_updated: datetime = Field(default_factory=datetime.now)

    user = User(username="bob")
    assert user.__fields_set__ == {"username"}
    user = User(username="bob", email="bob@test.com")
    assert user.__fields_set__ == {"username", "email"}
    user = User(
        username="bob",
        email="bob@test.com",
        last_updated=datetime.now() - timedelta(days=1),
    )
    assert user.__fields_set__ == {"username", "email", "last_updated"}
