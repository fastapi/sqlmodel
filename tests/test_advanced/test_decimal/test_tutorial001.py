import importlib
import types
from decimal import Decimal
from unittest.mock import MagicMock # Keep MagicMock for type hint, though not strictly necessary for runtime

import pytest
from sqlmodel import create_engine

from ...conftest import needs_py310, PrintMock # Import PrintMock for type hint

expected_calls = [
    [
        "Hero 1:",
        {
            "name": "Deadpond",
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "money": Decimal("1.100"),
        },
    ],
    [
        "Hero 2:",
        {
            "name": "Rusty-Man",
            "age": 48,
            "id": 3,
            "secret_name": "Tommy Sharp",
            "money": Decimal("2.200"),
        },
    ],
    ["Total money: 3.300"],
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest):
    module_name = request.param
    return importlib.import_module(f"docs_src.advanced.decimal.{module_name}")


def test_tutorial(print_mock: PrintMock, module: types.ModuleType):
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    module.main()
    assert print_mock.calls == expected_calls # Use .calls instead of .mock_calls
