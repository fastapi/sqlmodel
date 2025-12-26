import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.offset_and_limit.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
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
