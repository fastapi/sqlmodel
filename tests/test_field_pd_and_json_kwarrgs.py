import pytest
from sqlmodel import Field, SQLModel


def test_json_schema_extra_applied():
    """test json_schema_extra is applied to the field"""

    class Item(SQLModel):
        name: str = Field(
            json_schema_extra={
                "example": "Sword of Power",
                "x-custom-key": "Important Data",
            }
        )

    schema = Item.model_json_schema()

    name_schema = schema["properties"]["name"]

    assert name_schema["example"] == "Sword of Power"
    assert name_schema["x-custom-key"] == "Important Data"


def test_pydantic_kwargs_applied():
    """test pydantic_kwargs is applied to the field"""

    class User(SQLModel):
        user_name: str = Field(pydantic_kwargs={"validation_alias": "UserNameInInput"})

    field_info = User.model_fields["user_name"]

    assert field_info.validation_alias == "UserNameInInput"

    data = {"UserNameInInput": "KimigaiiWuyi"}
    user = User.model_validate(data)
    assert user.user_name == "KimigaiiWuyi"


def test_schema_extra_and_new_param_conflict():
    with pytest.raises(RuntimeError) as excinfo:

        class ItemA(SQLModel):
            name: str = Field(
                schema_extra={"legacy": 1},
                json_schema_extra={"new": 2},
            )

    assert "Passing schema_extra is not supported" in str(excinfo.value)

    with pytest.raises(RuntimeError) as excinfo:

        class ItemB(SQLModel):
            name: str = Field(
                schema_extra={"legacy": 1},
                pydantic_kwargs={"alias": "Alias"},
            )

    assert "Passing schema_extra is not supported" in str(excinfo.value)


def test_schema_extra_backward_compatibility():
    """
    test that schema_extra is backward compatible with json_schema_extra
    """

    # 1. 定义一个仅使用 schema_extra 的模型
    class LegacyItem(SQLModel):
        name: str = Field(
            schema_extra={
                "example": "Sword of Old",
                "x-custom-key": "Important Data",
                "serialization_alias": "id_test",
            }
        )

    schema = LegacyItem.model_json_schema()

    name_schema = schema["properties"]["name"]

    assert name_schema["example"] == "Sword of Old"
    assert name_schema["x-custom-key"] == "Important Data"

    field_info = LegacyItem.model_fields["name"]
    assert field_info.serialization_alias == "id_test"
