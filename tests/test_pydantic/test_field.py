from decimal import Decimal
from typing import Literal, Optional, Union

import pytest
from pydantic import ConfigDict, ValidationError
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


def test_alias_priority_1():
    def to_camel(string: str) -> str:
        return "".join(word.capitalize() for word in string.split("_"))

    class Model(SQLModel):
        model_config = ConfigDict(alias_generator=to_camel)

        field: str = Field(alias="field_alias", alias_priority=1)

    m = Model.model_validate({"Field": "value1"})
    assert m.field == "value1"

    with pytest.raises(ValidationError):
        Model.model_validate({"field_alias": "value1"})


@pytest.mark.parametrize("alias_priority", [None, 2])
def test_alias_priority_2(alias_priority: Optional[int]):
    def to_camel(string: str) -> str:
        return "".join(word.capitalize() for word in string.split("_"))

    class Model(SQLModel):
        model_config = ConfigDict(alias_generator=to_camel)

        field: str = Field(alias="field_alias", alias_priority=alias_priority)

    m = Model.model_validate({"field_alias": "value1"})
    assert m.field == "value1"

    with pytest.raises(ValidationError):
        Model.model_validate({"Field": "value1"})


def test_alias_priority_via_schema_extra():  # Current workaround. Remove after some time
    def to_camel(string: str) -> str:
        return "".join(word.capitalize() for word in string.split("_"))

    with pytest.warns(
        DeprecationWarning,
        match="Pass `alias_priority` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            model_config = ConfigDict(alias_generator=to_camel)

            field: str = Field(alias="field_alias", schema_extra={"alias_priority": 2})

    m = Model.model_validate({"field_alias": "value1"})
    assert m.field == "value1"

    with pytest.raises(ValidationError):
        Model.model_validate({"Field": "value1"})
