from datetime import datetime, timedelta

from sqlmodel import Field, SQLModel


def test_fields_set():
    class User(SQLModel):
        username: str
        email: str = "test@test.com"
        last_updated: datetime = Field(default_factory=datetime.now)

    user = User(username="bob")
    assert user.model_fields_set == {"username"}
    user = User(username="bob", email="bob@test.com")
    assert user.model_fields_set == {"username", "email"}
    user = User(
        username="bob",
        email="bob@test.com",
        last_updated=datetime.now() - timedelta(days=1),
    )
    assert user.model_fields_set == {"username", "email", "last_updated"}
