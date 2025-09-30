from typing import Type, Union

import pytest
from pydantic import VERSION, BaseModel, ValidationError
from pydantic import Field as PField
from sqlmodel import Field, SQLModel

# -----------------------------------------------------------------------------------
# Models


class PydanticUser(BaseModel):
    full_name: str = PField(alias="fullName")


class SQLModelUser(SQLModel):
    full_name: str = Field(alias="fullName")


# Models with config (validate_by_name=True)


if VERSION.startswith("2."):

    class PydanticUserWithConfig(PydanticUser):
        model_config = {"validate_by_name": True}

    class SQLModelUserWithConfig(SQLModelUser):
        model_config = {"validate_by_name": True}

else:

    class PydanticUserWithConfig(PydanticUser):
        class Config:
            allow_population_by_field_name = True

    class SQLModelUserWithConfig(SQLModelUser):
        class Config:
            allow_population_by_field_name = True


# -----------------------------------------------------------------------------------
# Tests

# Test validate by name


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_create_with_field_name(model: Union[Type[PydanticUser], Type[SQLModelUser]]):
    with pytest.raises(ValidationError):
        model(full_name="Alice")


@pytest.mark.parametrize("model", [PydanticUserWithConfig, SQLModelUserWithConfig])
def test_create_with_field_name_with_config(
    model: Union[Type[PydanticUserWithConfig], Type[SQLModelUserWithConfig]],
):
    user = model(full_name="Alice")
    assert user.full_name == "Alice"


# Test validate by alias


@pytest.mark.parametrize(
    "model",
    [PydanticUser, SQLModelUser, PydanticUserWithConfig, SQLModelUserWithConfig],
)
def test_create_with_alias(
    model: Union[
        Type[PydanticUser],
        Type[SQLModelUser],
        Type[PydanticUserWithConfig],
        Type[SQLModelUserWithConfig],
    ],
):
    user = model(fullName="Bob")  # using alias
    assert user.full_name == "Bob"


# Test validate by name and alias


@pytest.mark.parametrize("model", [PydanticUserWithConfig, SQLModelUserWithConfig])
def test_create_with_both_prefers_alias(
    model: Union[Type[PydanticUserWithConfig], Type[SQLModelUserWithConfig]],
):
    user = model(full_name="IGNORED", fullName="Charlie")
    assert user.full_name == "Charlie"  # alias should take precedence


# Test serialize


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_dict_default_uses_field_names(
    model: Union[Type[PydanticUser], Type[SQLModelUser]],
):
    user = model(fullName="Dana")
    data = user.dict()
    assert "full_name" in data
    assert "fullName" not in data
    assert data["full_name"] == "Dana"


# Test serialize by alias


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_dict_default_uses_aliases(
    model: Union[Type[PydanticUser], Type[SQLModelUser]],
):
    user = model(fullName="Dana")
    data = user.dict(by_alias=True)
    assert "fullName" in data
    assert "full_name" not in data
    assert data["fullName"] == "Dana"


# Test json by alias


@pytest.mark.parametrize("model", [PydanticUser, SQLModelUser])
def test_json_by_alias(
    model: Union[Type[PydanticUser], Type[SQLModelUser]],
):
    user = model(fullName="Frank")
    json_data = user.json(by_alias=True)
    assert ('"fullName":"Frank"' in json_data) or ('"fullName": "Frank"' in json_data)
    assert "full_name" not in json_data


# Pydantic v2 specific models - only define if we're running Pydantic v2
if VERSION.startswith("2."):

    class PydanticUserV2(BaseModel):
        first_name: str = PField(
            validation_alias="firstName", serialization_alias="f_name"
        )

    class SQLModelUserV2(SQLModel):
        first_name: str = Field(
            validation_alias="firstName", serialization_alias="f_name"
        )
else:
    # Dummy classes for Pydantic v1 to prevent import errors
    PydanticUserV2 = None
    SQLModelUserV2 = None


@needs_pydanticv2
@pytest.mark.parametrize("model", [PydanticUserV2, SQLModelUserV2])
def test_create_with_validation_alias(
    model: Union[Type[PydanticUserV2], Type[SQLModelUserV2]],
):
    user = model(firstName="John")
    assert user.first_name == "John"


@pytest.mark.skipif(
    not VERSION.startswith("2."),
    reason="validation_alias and serialization_alias are not supported in Pydantic v1",
)
@pytest.mark.parametrize("model", [PydanticUserV2, SQLModelUserV2])
def test_serialize_with_serialization_alias(
    model: Union[Type[PydanticUserV2], Type[SQLModelUserV2]],
):
    user = model(firstName="Jane")
    data = user.dict(by_alias=True)
    assert "f_name" in data
    assert "firstName" not in data
    assert "first_name" not in data
    assert data["f_name"] == "Jane"
