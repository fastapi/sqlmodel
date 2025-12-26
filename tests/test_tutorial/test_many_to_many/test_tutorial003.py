import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.many_to_many.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


expected_calls = [
    [
        "Z-Force hero:",
        {"name": "Deadpond", "secret_name": "Dive Wilson", "id": 1, "age": None},
        "is training:",
        False,
    ],
    [
        "Preventers hero:",
        {"name": "Deadpond", "secret_name": "Dive Wilson", "id": 1, "age": None},
        "is training:",
        True,
    ],
    [
        "Preventers hero:",
        {"name": "Spider-Boy", "secret_name": "Pedro Parqueador", "id": 2, "age": None},
        "is training:",
        True,
    ],
    [
        "Preventers hero:",
        {"name": "Rusty-Man", "secret_name": "Tommy Sharp", "id": 3, "age": 48},
        "is training:",
        False,
    ],
    [
        "Updated Spider-Boy's Teams:",
        [
            {"team_id": 2, "is_training": True, "hero_id": 2},
            {"team_id": 1, "is_training": True, "hero_id": 2},
        ],
    ],
    [
        "Z-Force heroes:",
        [
            {"team_id": 1, "is_training": False, "hero_id": 1},
            {"team_id": 1, "is_training": True, "hero_id": 2},
        ],
    ],
    [
        "Spider-Boy team:",
        {"headquarters": "Sharp Tower", "id": 2, "name": "Preventers"},
        "is training:",
        False,
    ],
    [
        "Spider-Boy team:",
        {"headquarters": "Sister Margaret's Bar", "id": 1, "name": "Z-Force"},
        "is training:",
        True,
    ],
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
