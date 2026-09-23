import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock

expected_calls = [
    [
        "Hero 1:",
        {"id": 2, "name": "Spider-Boy", "secret_name": "Pedro Parqueador", "age": None},
    ],
    [
        "Hero 2:",
        {
            "id": 7,
            "name": "Captain North America",
            "secret_name": "Esteban Rogelios",
            "age": 93,
        },
    ],
    [
        "Updated hero 1:",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    [
        "Updated hero 2:",
        {
            "id": 7,
            "name": "Captain North America Except Canada",
            "secret_name": "Esteban Rogelios",
            "age": 110,
        },
    ],
]


@pytest.fixture(name="module")
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    module = importlib.import_module(f"docs_src.tutorial.update.{request.param}")
    module.engine = database_engine
    return module


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial003_py310"),
    ],
    indirect=True,
)
def test_tutorial003(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial004_py310"),
    ],
    indirect=True,
)
def test_tutorial004(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls
