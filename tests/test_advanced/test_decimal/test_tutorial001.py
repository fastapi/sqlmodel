import importlib
from decimal import Decimal
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.advanced.decimal.{request.param}")
    mod.engine = database_engine
    return mod


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


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
