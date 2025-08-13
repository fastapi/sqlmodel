import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, get_testing_print_function, needs_py39, needs_py310

expected_calls_tutorial003 = [  # Renamed for specificity
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


@pytest.fixture(
    name="module",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py39", marks=needs_py39),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.many_to_many.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
        pass
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == expected_calls_tutorial003
