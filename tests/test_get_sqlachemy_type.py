from typing import Any, Dict, List, Union
from unittest.mock import MagicMock

import pytest
from pydantic.fields import ModelField
from sqlmodel.main import get_sqlachemy_type


@pytest.mark.parametrize(
    "input_type",
    [
        List[str],
        Dict[str, Any],
        Union[int, str],
    ],
)
def test_non_type_does_not_break(input_type: type) -> None:
    model_field_mock = MagicMock(ModelField, type_=input_type)
    with pytest.raises(ValueError):
        get_sqlachemy_type(model_field_mock)
