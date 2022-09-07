"""
Tests to ensure that the SQLModel `Field` constructor works as
expected from the Pydantic `Field` function.
"""
import sys
from decimal import Decimal
from typing import List, Optional, Union

import pytest
from pydantic import ValidationError
from sqlmodel import Field, SQLModel


def test_decimal():
    class Model(SQLModel):
        dec: Decimal = Field(max_digits=4, decimal_places=2)

    Model(dec=Decimal("3.14"))
    Model(dec=Decimal("69.42"))

    with pytest.raises(ValidationError):
        Model(dec=Decimal("3.142"))
    with pytest.raises(ValidationError):
        Model(dec=Decimal("0.069"))
    with pytest.raises(ValidationError):
        Model(dec=Decimal("420"))


def test_unique_items():
    class Model(SQLModel):
        unique_strings: List[str] = Field(unique_items=True)

    Model(unique_strings=["x", "y"])

    with pytest.raises(ValidationError):
        Model(unique_strings=["x", "y", "x"])


@pytest.mark.skipif(
    sys.version_info < (3, 8), reason="requires Python 3.8+ (for `typing.Literal`)"
)
def test_discriminator():
    from typing import Literal

    # Example adapted from
    # [Pydantic docs](https://pydantic-docs.helpmanual.io/usage/types/#discriminated-unions-aka-tagged-unions):

    class Cat(SQLModel):
        pet_type: Literal["cat"]
        meows: int

    class Dog(SQLModel):
        pet_type: Literal["dog"]
        barks: float

    class Lizard(SQLModel):
        pet_type: Literal["reptile", "lizard"]
        scales: bool

    class Model(SQLModel):
        pet: Union[Cat, Dog, Lizard] = Field(..., discriminator="pet_type")
        n: int

    Model(pet={"pet_type": "dog", "barks": 3.14}, n=1)  # type: ignore[arg-type]

    with pytest.raises(ValidationError):
        Model(pet={"pet_type": "dog"}, n=1)  # type: ignore[arg-type]


def test_repr():
    class Model(SQLModel):
        id: Optional[int] = Field(primary_key=True)
        foo: str = Field(repr=False)

    instance = Model(id=123, foo="bar")
    assert "foo=" not in repr(instance)
