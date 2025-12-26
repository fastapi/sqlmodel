import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310

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
    [
        "Hero: ",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    [
        "Deleted hero:",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    ["There's no hero named Spider-Youngster"],
]


@pytest.fixture(name="module")
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(f"docs_src.tutorial.delete.{request.param}")
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    return module


@pytest.mark.parametrize(
    "module",
    [
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial001(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls


@pytest.mark.parametrize(
    "module",
    [
        "tutorial002_py39",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial002(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls
