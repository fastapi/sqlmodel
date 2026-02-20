from decimal import Decimal
from typing import Any, Literal

import pytest
from pydantic import ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine


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
        pet: Cat | Dog | Lizard = Field(..., discriminator="pet_type")
        n: int

    Model(pet={"pet_type": "dog", "barks": 3.14}, n=1)  # type: ignore[arg-type]

    with pytest.raises(ValidationError):
        Model(pet={"pet_type": "dog"}, n=1)  # type: ignore[arg-type]


def test_repr():
    class Model(SQLModel):
        id: int | None = Field(primary_key=True)
        foo: str = Field(repr=False)

    instance = Model(id=123, foo="bar")
    assert "foo=" not in repr(instance)


def test_strict_true():
    class Model(SQLModel):
        id: int | None = Field(default=None, primary_key=True)
        val: int
        val_strict: int = Field(strict=True)

    class ModelDB(Model, table=True):
        pass

    Model(val=123, val_strict=456)
    Model(val="123", val_strict=456)

    with pytest.raises(ValidationError):
        Model(val=123, val_strict="456")

    engine = create_engine("sqlite://", echo=True)

    SQLModel.metadata.create_all(engine)

    model = ModelDB(val=123, val_strict=456)
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)

    assert model.val == 123
    assert model.val_strict == 456


def test_strict_table_model():
    class Model(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        val_strict: int = Field(strict=True)

    engine = create_engine("sqlite://", echo=True)

    SQLModel.metadata.create_all(engine)

    model = Model(val_strict=456)
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)

    assert model.val_strict == 456


@pytest.mark.parametrize("strict", [None, False])
def test_strict_false(strict: int | None):
    class Model(SQLModel):
        val: int = Field(strict=strict)

    Model(val=123)
    Model(val="123")


def test_strict_via_schema_extra():  # Current workaround. Remove after some time
    with pytest.warns(
        DeprecationWarning,
        match="Pass `strict` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            val: int
            val_strict: int = Field(schema_extra={"strict": True})

    Model(val=123, val_strict=456)
    Model(val="123", val_strict=456)

    with pytest.raises(ValidationError):
        Model(val=123, val_strict="456")


def test_examples():
    class Model(SQLModel):
        name: str = Field(examples=["Alice", "Bob"])

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["name"]["examples"] == ["Alice", "Bob"]


def test_examples_via_schema_extra():  # Current workaround. Remove after some time
    with pytest.warns(
        DeprecationWarning,
        match="Pass `examples` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            name: str = Field(schema_extra={"examples": ["Alice", "Bob"]})

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["name"]["examples"] == ["Alice", "Bob"]


def test_deprecated():
    class Model(SQLModel):
        old_field: str = Field(deprecated=True)
        another_old_field: str = Field(deprecated="This field is deprecated")

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["old_field"]["deprecated"] is True
    assert model_schema["properties"]["another_old_field"]["deprecated"] is True


def test_deprecated_via_schema_extra():  # Current workaround. Remove after some time
    with pytest.warns(
        DeprecationWarning,
        match="Pass `deprecated` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            old_field: str = Field(schema_extra={"deprecated": True})
            another_old_field: str = Field(
                schema_extra={"deprecated": "This field is deprecated"}
            )

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["old_field"]["deprecated"] is True
    assert model_schema["properties"]["another_old_field"]["deprecated"] is True


def test_exclude_if():
    def is_empty_string(value: Any) -> bool:
        return value == ""

    class Model(SQLModel):
        name: str = Field(exclude_if=is_empty_string)
        age: int

    model1 = Model(name="Alice", age=30)
    model2 = Model(name="", age=25)

    dict1 = model1.model_dump()
    dict2 = model2.model_dump()

    assert "name" in dict1
    assert dict1["name"] == "Alice"

    assert "name" not in dict2


def test_exclude_if_via_schema_extra():
    def is_empty_string(value: Any) -> bool:
        return value == ""

    with pytest.warns(
        DeprecationWarning,
        match="Pass `exclude_if` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            name: str = Field(schema_extra={"exclude_if": is_empty_string})
            age: int

    model1 = Model(name="Alice", age=30)
    model2 = Model(name="", age=25)

    dict1 = model1.model_dump()
    dict2 = model2.model_dump()

    assert "name" in dict1
    assert dict1["name"] == "Alice"

    assert "name" not in dict2


def test_field_title_generator():
    def upper(value: str, _: Any) -> str:
        return value.upper()

    class Model(SQLModel):
        name: str = Field(field_title_generator=upper)
        age: int

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["name"]["title"] == "NAME"
    assert model_schema["properties"]["age"]["title"] == "Age"


def test_field_title_generator_via_schema_extra():
    def upper(value: str, _: Any) -> str:
        return value.upper()

    with pytest.warns(
        DeprecationWarning,
        match="Pass `field_title_generator` parameter directly to Field instead of passing it via `schema_extra`",
    ):

        class Model(SQLModel):
            name: str = Field(schema_extra={"field_title_generator": upper})
            age: int

    model_schema = Model.model_json_schema()
    assert model_schema["properties"]["name"]["title"] == "NAME"
    assert model_schema["properties"]["age"]["title"] == "Age"
