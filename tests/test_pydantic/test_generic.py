from typing import Generic, List, Optional, TypeVar

import pydantic
import pytest
from sqlmodel import SQLModel

from tests.conftest import needs_pydanticv2

# Example adapted from
# https://docs.pydantic.dev/2.10/concepts/models/#generic-models
DataT = TypeVar("DataT")


class DataModel(SQLModel):
    numbers: List[int]
    people: List[str]


class Response(SQLModel, Generic[DataT]):
    data: Optional[DataT] = None


@needs_pydanticv2
@pytest.mark.parametrize(
    ["data_type", "data_value"],
    [
        (int, 1),
        (str, "value"),
        (DataModel, DataModel(numbers=[1, 2, 3], people=[])),
        (DataModel, {"numbers": [1, 2, 3], "people": []}),
    ],
)
def test_valid_generics(data_type, data_value):
    # Should be able to create a model without an error.
    response = Response[data_type](data=data_value)
    assert Response[data_type](**response.model_dump()) == response


@needs_pydanticv2
@pytest.mark.parametrize(
    ["data_type", "data_value", "error_loc", "error_type"],
    [
        (
            str,
            1,
            ("data",),
            "string_type",
        ),
        (
            int,
            "some-string",
            ("data",),
            "int_parsing",
        ),
        (
            DataModel,
            "some-string",
            ("data",),
            "model_attributes_type",
        ),
        (
            DataModel,
            {"numbers": [1, 2, "unexpected string"], "people": []},
            ("data", "numbers", 2),
            "int_parsing",
        ),
    ],
)
def test_invalid_generics(data_type, data_value, error_loc, error_type):
    with pytest.raises(pydantic.ValidationError) as raised:
        Response[data_type](data=data_value)
    [error_dict] = raised.value.errors()
    assert error_dict["loc"] == error_loc
    assert error_dict["type"] == error_type
