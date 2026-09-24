import importlib
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
    mod = importlib.import_module(f"docs_src.tutorial.offset_and_limit.{request.param}")
    mod.engine = database_engine
    return mod


expected_calls = [
    [
        [
            {"id": 1, "name": "Deadpond", "secret_name": "Dive Wilson", "age": None},
            {
                "id": 2,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "age": None,
            },
            {"id": 3, "name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48},
        ]
    ]
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
