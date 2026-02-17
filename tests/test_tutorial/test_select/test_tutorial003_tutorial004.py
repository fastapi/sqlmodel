import importlib
from types import ModuleType
from typing import Any, Union

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


def check_calls(calls: list[list[Union[str, dict[str, Any]]]]):
    assert calls[0][0] == [
        {
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
            "id": 1,
        },
        {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
            "id": 2,
        },
        {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
            "id": 3,
        },
    ]


@pytest.fixture(name="module")
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(f"docs_src.tutorial.select.{request.param}")
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    return module


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial_003(print_mock: PrintMock, module: ModuleType):
    module.main()
    check_calls(print_mock.calls)


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial_004(print_mock: PrintMock, module: ModuleType):
    module.main()
    check_calls(print_mock.calls)
