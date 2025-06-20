import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine, SQLModel

from ....conftest import get_testing_print_function, needs_py39, needs_py310, PrintMock


expected_calls_tutorial001 = [
    [
        "Created hero:",
        {
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "team_id": 1,
            "id": 1,
            "age": None,
        },
    ],
    [
        "Created hero:",
        {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "team_id": 2,
            "id": 2,
            "age": 48,
        },
    ],
    [
        "Created hero:",
        {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "id": 3,
            "age": None,
        },
    ],
    [
        "Updated hero:",
        {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
            "id": 3,
            "age": None,
        },
    ],
    [
        "Team Wakaland:",
        {"name": "Wakaland", "id": 3, "headquarters": "Wakaland Capital City"},
    ],
    [
        "Deleted team:",
        {"name": "Wakaland", "id": 3, "headquarters": "Wakaland Capital City"},
    ],
    ["Black Lion not found:", None],
    ["Princess Sure-E not found:", None],
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py39", marks=needs_py39),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    # Using the corrected docs_src path
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

    assert print_mock.calls == expected_calls_tutorial001
