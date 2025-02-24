import datetime
from decimal import Decimal
from typing import Annotated, Optional, Union

import pytest
import sqlalchemy as sa
from pydantic import ValidationError
from sqlmodel import Field, SQLModel
from sqlmodel.main import FieldInfo
from typing_extensions import Literal


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


def test_field_merging():
    sa_type = sa.DATETIME

    MyDateTime = Annotated[
        datetime.datetime,
        Field(sa_type=sa_type),
    ]

    class Model(SQLModel):
        value: Annotated[
            MyDateTime,
            Field(default_factory=datetime.datetime.now),
            Field(description="some-description", title="some-title"),
            Field(index=True),
        ] = Field(nullable=False)

    assert Model.model_json_schema() == {
        "properties": {
            "value": {
                "description": "some-description",
                "format": "date-time",
                "title": "some-title",
                "type": "string",
            }
        },
        "title": "Model",
        "type": "object",
    }
    expected_field = Field(
        sa_type=sa.DATETIME,
        default_factory=datetime.datetime.now,
        description="some-description",
        title="some-title",
        index=True,
        nullable=False,
    )
    actual_field = Model.model_fields["value"]
    assert isinstance(actual_field, FieldInfo)

    comp_attrs = [
        "sa_type",
        "default_factory",
        "description",
        "title",
        "index",
        "nullable",
    ]
    for attr in comp_attrs:
        assert getattr(actual_field, attr) == getattr(expected_field, attr)
        assert getattr(actual_field, attr) is not None
