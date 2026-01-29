from decimal import Decimal
from typing import Annotated, Any, Literal, Optional, Union

import pytest
from pydantic import ValidationError
from sqlmodel import Discriminator, Field, SQLModel, Tag


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


def test_discriminator_callable():
    # Example adapted from
    # [Pydantic docs](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-callable-discriminator):

    class Pie(SQLModel):
        pass

    class ApplePie(Pie):
        fruit: Literal["apple"] = "apple"

    class PumpkinPie(Pie):
        filling: Literal["pumpkin"] = "pumpkin"

    def get_discriminator_value(v: Any) -> str:
        if isinstance(v, dict):
            return v.get("fruit", v.get("filling"))
        return getattr(v, "fruit", getattr(v, "filling", None))

    class ThanksgivingDinner(SQLModel):
        dessert: Union[
            Annotated[ApplePie, Tag("apple")],
            Annotated[PumpkinPie, Tag("pumpkin")],
        ] = Field(
            discriminator=Discriminator(get_discriminator_value),
        )

    apple_pie = ThanksgivingDinner.model_validate({"dessert": {"fruit": "apple"}})
    assert isinstance(apple_pie.dessert, ApplePie)

    pumpkin_pie = ThanksgivingDinner.model_validate({"dessert": {"filling": "pumpkin"}})
    assert isinstance(pumpkin_pie.dessert, PumpkinPie)


def test_repr():
    class Model(SQLModel):
        id: Optional[int] = Field(primary_key=True)
        foo: str = Field(repr=False)

    instance = Model(id=123, foo="bar")
    assert "foo=" not in repr(instance)
