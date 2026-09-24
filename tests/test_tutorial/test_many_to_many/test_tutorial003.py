import importlib
from types import ModuleType

import pytest
from dirty_equals import IsList
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.many_to_many.{request.param}")
    mod.engine = database_engine
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
        IsList(
            {"team_id": 2, "is_training": True, "hero_id": 2},
            {"team_id": 1, "is_training": True, "hero_id": 2},
            check_order=False,
        ),
    ],
    [
        "Z-Force heroes:",
        IsList(
            {"team_id": 1, "is_training": False, "hero_id": 1},
            {"team_id": 1, "is_training": True, "hero_id": 2},
            check_order=False,
        ),
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
    assert print_mock.calls[:1] == expected_calls[:1]
    assert print_mock.calls[1:4] == IsList(*expected_calls[1:4], check_order=False)
    assert print_mock.calls[4:6] == expected_calls[4:6]
    assert print_mock.calls[6:] == IsList(*expected_calls[6:], check_order=False)
