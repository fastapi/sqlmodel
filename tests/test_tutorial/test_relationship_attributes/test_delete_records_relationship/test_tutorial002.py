import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine, SQLModel

from ....conftest import get_testing_print_function, needs_py39, needs_py310, PrintMock


expected_calls_tutorial002 = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "team_id": 1,
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "team_id": 2,
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": None,
        },
    ],
    [
        "Updated hero:",
        {
            "age": None,
            "id": 3,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
        },
    ],
    [
        "Team Wakaland:",
        {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
    ],
    [
        "Deleted team:",
        {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
    ],
    [
        "Black Lion has no team:",
        {
            "age": 35,
            "id": 4,
            "name": "Black Lion",
            "secret_name": "Trevor Challa",
            "team_id": None,
        },
    ],
    [
        "Princess Sure-E has no team:",
        {
            "age": None,
            "id": 5,
            "name": "Princess Sure-E",
            "secret_name": "Sure-E",
            "team_id": None,
        },
    ],
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial002",
        pytest.param("tutorial002_py39", marks=needs_py39),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.relationship_attributes.cascade_delete_relationships.{module_name}"

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

    assert print_mock.calls == expected_calls_tutorial002
