import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine

# Assuming conftest.py is at tests/conftest.py, the path should be ....conftest
from ....conftest import PrintMock, get_testing_print_function, needs_py39, needs_py310

expected_calls_tutorial001 = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 1,
            "name": "Deadpond",
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 2,
            "name": "Rusty-Man",
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "name": "Spider-Boy",
        },
    ],
    [
        "Updated hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
            "name": "Spider-Boy",
        },
    ],
    [
        "Team Wakaland:",
        {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
    ],
    [
        "Preventers new hero:",
        {
            "age": 32,
            "id": 6,
            "secret_name": "Natalia Roman-on",
            "team_id": 2,
            "name": "Tarantula",
        },
    ],
    [
        "Preventers new hero:",
        {
            "age": 36,
            "id": 7,
            "secret_name": "Steve Weird",
            "team_id": 2,
            "name": "Dr. Weird",
        },
    ],
    [
        "Preventers new hero:",
        {
            "age": 93,
            "id": 8,
            "secret_name": "Esteban Rogelios",
            "team_id": 2,
            "name": "Captain North America",
        },
    ],
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
    full_module_name = f"docs_src.tutorial.relationship_attributes.create_and_update_relationships.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
        # Assuming main() or create_db_and_tables() handles table creation
        pass
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == expected_calls_tutorial001
