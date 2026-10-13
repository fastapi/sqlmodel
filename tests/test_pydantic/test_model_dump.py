from typing import Any

import pytest
from sqlmodel import SQLModel
from sqlmodel._compat import PYDANTIC_MINOR_VERSION


@pytest.mark.parametrize(
    ("polymorphic_serialization", "expected_result"),
    [
        (None, {"user": {"name": "pydantic"}}),
        (False, {"user": {"name": "pydantic"}}),
        pytest.param(
            True,
            {"user": {"name": "pydantic", "password": "password"}},
            marks=pytest.mark.skipif(
                PYDANTIC_MINOR_VERSION < (2, 13),
                reason="polymorphic_serialization is only available in Pydantic v2.13+",
            ),
        ),
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

    assert outer_model.model_dump(polymorphic_serialization=False) == {
        "user": {"name": "pydantic"}
    }
