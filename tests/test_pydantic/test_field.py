from decimal import Decimal
from typing import Literal, Optional, Union

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


def test_discriminator():
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


def test_min_items():
    with pytest.warns(
        DeprecationWarning,
        match="`min_items` is deprecated and will be removed, use `min_length` instead",
    ):

        class Model(SQLModel):
            items: list[int] = Field(min_items=2)

    Model(items=[1, 2])

    with pytest.raises(ValidationError) as exc_info:
        Model(items=[1])
    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["type"] == "too_short"


def test_max_items():
    with pytest.warns(
        DeprecationWarning,
        match="`max_items` is deprecated and will be removed, use `max_length` instead",
    ):

        class Model(SQLModel):
            items: list[int] = Field(max_items=2)

    Model(items=[1, 2])

    with pytest.raises(ValidationError) as exc_info:
        Model(items=[1, 2, 3])
    assert len(exc_info.value.errors()) == 1
    assert exc_info.value.errors()[0]["type"] == "too_long"
