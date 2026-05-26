from typing import Any

import pytest
from sqlmodel import SQLModel


@pytest.mark.parametrize(
    ("polymorphic_serialization", "expected_result"),
    [
        (None, {"user": {"name": "pydantic"}}),
        (False, {"user": {"name": "pydantic"}}),
        (True, {"user": {"name": "pydantic", "password": "password"}}),
    ],
)
def test_polymorphic_serialization(
    polymorphic_serialization: bool | None, expected_result: dict[str, Any]
):

    class User(SQLModel):
        name: str

    class UserLogin(User):
        password: str

    class OuterModel(SQLModel):
        user: User

    outer_model = OuterModel(
        user=UserLogin(name="pydantic", password="password"),
    )

    assert (
        outer_model.model_dump(polymorphic_serialization=polymorphic_serialization)
        == expected_result
    )
