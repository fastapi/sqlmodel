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


def test_schema_extra_and_new_param_conflict(caplog):
    """
    Test that passing schema_extra and json_schema_extra at the same time produces
    a warning.
    """

    with pytest.warns(DeprecationWarning, match="schema_extra parameter is deprecated"):
        Field(schema_extra={"legacy": 1}, json_schema_extra={"new": 2})


def test_schema_extra_backward_compatibility():
    """
    test that schema_extra is backward compatible with json_schema_extra
    """

    with pytest.warns(DeprecationWarning, match="schema_extra parameter is deprecated"):

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


def test_json_schema_extra_mix_in_schema_extra():
    """test that json_schema_extra is applied when it is in schema_extra"""

    with pytest.warns(DeprecationWarning, match="schema_extra parameter is deprecated"):

        class Item(SQLModel):
            name: str = Field(
                schema_extra={
                    "json_schema_extra": {
                        "example": "Sword of Power",
                        "x-custom-key": "Important Data",
                    },
                    "serialization_alias": "id_test",
                }
            )

    schema = Item.model_json_schema()

    name_schema = schema["properties"]["name"]
    assert name_schema["example"] == "Sword of Power"
    assert name_schema["x-custom-key"] == "Important Data"

    field_info = Item.model_fields["name"]
    assert field_info.serialization_alias == "id_test"
