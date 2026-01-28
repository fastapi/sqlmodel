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


def test_coerce_numbers_to_str_true():
    class Model(SQLModel):
        val: str = Field(coerce_numbers_to_str=True)

    assert Model.model_validate({"val": 123}).val == "123"
    assert Model.model_validate({"val": 45.67}).val == "45.67"


@pytest.mark.parametrize("coerce_numbers_to_str", [None, False])
def test_coerce_numbers_to_str_false(coerce_numbers_to_str: Optional[bool]):
    class Model2(SQLModel):
        val: str = Field(coerce_numbers_to_str=coerce_numbers_to_str)

    with pytest.raises(ValidationError):
        Model2.model_validate({"val": 123})


def test_coerce_numbers_to_str_via_schema_extra():  # Current workaround. Remove after some time
    with pytest.warns(
        UserWarning,
        match=(
            "Pass `coerce_numbers_to_str` parameter directly to Field instead of passing "
            "it via `schema_extra`"
        ),
    ):

        class Model(SQLModel):
            val: str = Field(schema_extra={"coerce_numbers_to_str": True})

    assert Model.model_validate({"val": 123}).val == "123"
    assert Model.model_validate({"val": 45.67}).val == "45.67"
