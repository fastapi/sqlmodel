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


def test_field_regex_param():
    with pytest.warns(DeprecationWarning, match="The `regex` parameter is deprecated"):

        class DateModel(SQLModel):
            date_1: str = Field(regex=r"^\d{2}-\d{2}-\d{4}$")

    DateModel(date_1="12-31-2024")

    with pytest.raises(ValidationError):
        DateModel(date_1="incorrect")


def test_field_pattern_param():
    class DateModel(SQLModel):
        date_1: str = Field(pattern=r"^\d{2}-\d{2}-\d{4}$")

    DateModel(date_1="12-31-2024")

    with pytest.raises(ValidationError):
        DateModel(date_1="incorrect")


def test_field_pattern_via_schema_extra():
    class DateModel(SQLModel):
        date_1: str = Field(schema_extra={"pattern": r"^\d{2}-\d{2}-\d{4}$"})

    with pytest.raises(ValidationError):
        DateModel(date_1="incorrect")
