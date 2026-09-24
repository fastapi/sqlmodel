import importlib
from types import ModuleType

import pytest
from dirty_equals import IsList
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.many_to_many.{request.param}")
    mod.engine = database_engine
    return mod


expected_calls = [
    [
        "Deadpond:",
        {"id": 1, "secret_name": "Dive Wilson", "age": None, "name": "Deadpond"},
    ],
    [
        "Deadpond teams:",
        IsList(
            {"id": 1, "name": "Z-Force", "headquarters": "Sister Margaret's Bar"},
            {"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"},
            check_order=False,
        ),
    ],
    [
        "Rusty-Man:",
        {"id": 2, "secret_name": "Tommy Sharp", "age": 48, "name": "Rusty-Man"},
    ],
    [
        "Rusty-Man Teams:",
        [{"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"}],
    ],
    [
        "Spider-Boy:",
        {"id": 3, "secret_name": "Pedro Parqueador", "age": None, "name": "Spider-Boy"},
    ],
    [
        "Spider-Boy Teams:",
        [{"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"}],
    ],
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
