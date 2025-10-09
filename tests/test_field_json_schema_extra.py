import pytest
from sqlmodel import Field, SQLModel
from sqlmodel._compat import IS_PYDANTIC_V2

from tests.conftest import needs_pydanticv2


def test_json_schema_extra_applied():
    """test json_schema_extra is applied to the field"""

    class Item(SQLModel):
        name: str = Field(
            json_schema_extra={
                "example": "Sword of Power",
                "x-custom-key": "Important Data",
            }
        )

    if IS_PYDANTIC_V2:
        schema = Item.model_json_schema()
    else:
        schema = Item.schema()

    name_schema = schema["properties"]["name"]

    assert name_schema["example"] == "Sword of Power"
    assert name_schema["x-custom-key"] == "Important Data"


def test_schema_extra_and_json_schema_extra_conflict():
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

    if IS_PYDANTIC_V2:
        schema = LegacyItem.model_json_schema()
    else:
        schema = LegacyItem.schema()

    name_schema = schema["properties"]["name"]

    assert name_schema["example"] == "Sword of Old"
    assert name_schema["x-custom-key"] == "Important Data"

    if IS_PYDANTIC_V2:
        # With Pydantic V1 serialization_alias from schema_extra is applied
        field_info = LegacyItem.model_fields["name"]
        assert field_info.serialization_alias == "id_test"
    else:  # With Pydantic V1 it just goes to schema
        assert name_schema["serialization_alias"] == "id_test"


@needs_pydanticv2
def test_json_schema_extra_mix_in_schema_extra():
    """
    Test workaround when json_schema_extra was passed via schema_extra with Pydantic v2.
    """

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
