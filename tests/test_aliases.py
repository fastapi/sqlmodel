from typing import Union

import pytest
from pydantic import BaseModel, ValidationError
from pydantic import Field as PField
from sqlmodel import Field, SQLModel

"""
Alias tests for SQLModel and Pydantic compatibility
"""


class PydanticUser(BaseModel):
    full_name: str = PField(alias="fullName")


class SQLModelUser(SQLModel):
    full_name: str = Field(alias="fullName")


# Models with config (validate_by_name=True)
class PydanticUserWithConfig(PydanticUser):
    model_config = {"validate_by_name": True}


class SQLModelUserWithConfig(SQLModelUser):
    model_config = {"validate_by_name": True}


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_create_with_field_name(model: Union[type[PydanticUser], type[SQLModelUser]]):
    with pytest.raises(ValidationError):
        model(full_name="Alice")


@pytest.mark.parametrize("model", [PydanticUserWithConfig, SQLModelUserWithConfig])
def test_create_with_field_name_with_config(
    model: Union[type[PydanticUserWithConfig], type[SQLModelUserWithConfig]],
):
    user = model(full_name="Alice")
    assert user.full_name == "Alice"


@pytest.mark.parametrize(
    "model",
    [PydanticUser, SQLModelUser, PydanticUserWithConfig, SQLModelUserWithConfig],
)
def test_create_with_alias(
    model: Union[
        type[PydanticUser],
        type[SQLModelUser],
        type[PydanticUserWithConfig],
        type[SQLModelUserWithConfig],
    ],
):
    user = model(fullName="Bob")  # using alias
    assert user.full_name == "Bob"


@pytest.mark.parametrize("model", [PydanticUserWithConfig, SQLModelUserWithConfig])
def test_create_with_both_prefers_alias(
    model: Union[type[PydanticUserWithConfig], type[SQLModelUserWithConfig]],
):
    user = model(full_name="IGNORED", fullName="Charlie")
    assert user.full_name == "Charlie"  # alias should take precedence


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_dict_default_uses_field_names(
    model: Union[type[PydanticUser], type[SQLModelUser]],
):
    user = model(fullName="Dana")
    data = user.model_dump()
    assert "full_name" in data
    assert "fullName" not in data
    assert data["full_name"] == "Dana"


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_dict_by_alias_uses_aliases(
    model: Union[type[PydanticUser], type[SQLModelUser]],
):
    user = model(fullName="Dana")
    data = user.model_dump(by_alias=True)
    assert "fullName" in data
    assert "full_name" not in data
    assert data["fullName"] == "Dana"


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_json_by_alias(
    model: Union[type[PydanticUser], type[SQLModelUser]],
):
    user = model(fullName="Frank")
    json_data = user.model_dump_json(by_alias=True)
    assert ('"fullName":"Frank"' in json_data) or ('"fullName": "Frank"' in json_data)
    assert "full_name" not in json_data


class PydanticUserV2(BaseModel):
    first_name: str = PField(validation_alias="firstName", serialization_alias="f_name")


class SQLModelUserV2(SQLModel):
    first_name: str = Field(validation_alias="firstName", serialization_alias="f_name")


@pytest.mark.parametrize("model", [PydanticUserV2, SQLModelUserV2])
def test_create_with_validation_alias(
    model: Union[type[PydanticUserV2], type[SQLModelUserV2]],
):
    user = model(firstName="John")
    assert user.first_name == "John"


@pytest.mark.parametrize("model", [PydanticUserV2, SQLModelUserV2])
def test_serialize_with_serialization_alias(
    model: Union[type[PydanticUserV2], type[SQLModelUserV2]],
):
    user = model(firstName="Jane")
    data = user.model_dump(by_alias=True)
    assert "f_name" in data
    assert "firstName" not in data
    assert "first_name" not in data
    assert data["f_name"] == "Jane"


def test_schema_extra_validation_alias_sqlmodel_v2():
    class M(SQLModel):
        f: str = Field(schema_extra={"validation_alias": "f_alias"})

    m = M.model_validate({"f_alias": "asd"})
    assert m.f == "asd"


def test_schema_extra_serialization_alias_sqlmodel_v2():
    class M(SQLModel):
        f: str = Field(schema_extra={"serialization_alias": "f_out"})

    m = M(f="x")
    data = m.model_dump(by_alias=True)
    assert "f_out" in data
    assert "f" not in data
    assert data["f_out"] == "x"


def test_alias_plus_validation_alias_prefers_validation_alias_sqlmodel_v2():
    class M(SQLModel):
        first_name: str = Field(alias="fullName", validation_alias="v_name")

    m = M.model_validate({"fullName": "A", "v_name": "B"})
    assert m.first_name == "B"


def test_alias_plus_serialization_alias_prefers_serialization_alias_sqlmodel_v2():
    class M(SQLModel):
        first_name: str = Field(alias="fullName", serialization_alias="f_name")

    m = M(fullName="Z")
    data = m.model_dump(by_alias=True)
    assert "f_name" in data
    assert "fullName" not in data
    assert data["f_name"] == "Z"


def test_alias_generator_works_sqlmodel_v2():
    class M(SQLModel):
        model_config = {"alias_generator": lambda s: "gen_" + s}
        f: str = Field()

    m = M.model_validate({"gen_f": "ok"})
    assert m.f == "ok"
    data = m.model_dump(by_alias=True)
    assert "gen_f" in data and data["gen_f"] == "ok"


def test_alias_generator_with_explicit_alias_prefers_field_alias_sqlmodel_v2():
    class M(SQLModel):
        model_config = {"alias_generator": lambda s: "gen_" + s}
        f: str = Field(alias="custom")

    m = M.model_validate({"custom": "ok"})
    assert m.f == "ok"
    data = m.model_dump(by_alias=True)
    assert "custom" in data and "gen_f" not in data
