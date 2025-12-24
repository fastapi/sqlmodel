import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.many_to_many.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


expected_calls = [
    [
        "Deadpond:",
        {"id": 1, "secret_name": "Dive Wilson", "age": None, "name": "Deadpond"},
    ],
    [
        "Deadpond teams:",
        [
            {"id": 1, "name": "Z-Force", "headquarters": "Sister Margaret's Bar"},
            {"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"},
        ],
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
    [
        "Updated Spider-Boy's Teams:",
        [
            {"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"},
            {"id": 1, "name": "Z-Force", "headquarters": "Sister Margaret's Bar"},
        ],
    ],
    [
        "Z-Force heroes:",
        [
            {"id": 1, "secret_name": "Dive Wilson", "age": None, "name": "Deadpond"},
            {
                "id": 3,
                "secret_name": "Pedro Parqueador",
                "age": None,
                "name": "Spider-Boy",
            },
        ],
    ],
    [
        "Reverted Z-Force's heroes:",
        [{"id": 1, "secret_name": "Dive Wilson", "age": None, "name": "Deadpond"}],
    ],
    [
        "Reverted Spider-Boy's teams:",
        [{"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"}],
    ],
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
