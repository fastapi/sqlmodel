import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine, SQLModel

from ...conftest import get_testing_print_function, needs_py39, needs_py310, PrintMock


expected_calls_tutorial001 = [ # Renamed for specificity
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
    full_module_name = f"docs_src.tutorial.many_to_many.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    # Many-to-many tutorials often have a create_db_and_tables() in main() or similar.
    # If not, this is a safeguard.
    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
        # This function should call SQLModel.metadata.create_all(engine)
        # We assume it's called by main() or the test setup is fine if it's not explicitly called here.
        pass
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
         mod.SQLModel.metadata.create_all(mod.engine) # Create all tables known to this module's metadata

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    # The main function in the tutorial module executes the core logic and print statements.
    # The module_fixture ensures the engine is set.
    # clear_sqlmodel ensures a clean database state.
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == expected_calls_tutorial001
