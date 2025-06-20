import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine

# Adjust the import path based on the file's new location or structure
from ....conftest import PrintMock, get_testing_print_function, needs_py39, needs_py310

expected_calls_tutorial001 = [
    [
        "Created hero:",
        {
            "name": "Deadpond",
            "age": None,
            "team_id": 1,
            "id": 1,
            "secret_name": "Dive Wilson",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Rusty-Man",
            "age": 48,
            "team_id": 2,
            "id": 2,
            "secret_name": "Tommy Sharp",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Spider-Boy",
            "age": None,
            "team_id": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
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
    full_module_name = f"docs_src.tutorial.relationship_attributes.define_relationship_attributes.{module_name}"

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
