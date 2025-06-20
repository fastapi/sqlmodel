import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine, SQLModel # Added SQLModel for potential use if main doesn't create tables

from ...conftest import get_testing_print_function, needs_py310, PrintMock


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any): # clear_sqlmodel ensures fresh DB state
    module_name = request.param
    full_module_name = f"docs_src.tutorial.indexes.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    # These tests usually define engine in their main() or globally.
    # We'll ensure it's set up for the test a standard way.
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url) # connect_args not typically in these non-FastAPI examples

    # Ensure tables are created. Some tutorials do it in main, others expect it externally.
    # If mod.main() is expected to create tables, this might be redundant but safe.
    # If Hero model is defined globally, SQLModel.metadata.create_all(mod.engine) can be used.
    if hasattr(mod, "Hero") and hasattr(mod.Hero, "metadata"):
         mod.Hero.metadata.create_all(mod.engine)
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"): # Fallback if Hero specific metadata not found
         mod.SQLModel.metadata.create_all(mod.engine)


    return mod


def test_tutorial(print_mock: PrintMock, module: types.ModuleType):
    # The engine is now set up by the fixture.
    # clear_sqlmodel is handled by the fixture too.

    # If main() also creates engine and tables, ensure it doesn't conflict.
    # For these print-based tests, main() usually contains the core logic to be tested.
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == [
        [{"secret_name": "Dive Wilson", "age": None, "id": 1, "name": "Deadpond"}]
    ]

    insp: Inspector = inspect(module.engine)
    # Ensure table name is correctly retrieved from the possibly reloaded module
    table_name = str(module.Hero.__tablename__)
    indexes = insp.get_indexes(table_name)

    expected_indexes = [
        {
            "name": "ix_hero_name",
            "dialect_options": {},
            "column_names": ["name"],
            "unique": 0,
        },
        {
            "name": "ix_hero_age",
            "dialect_options": {},
            "column_names": ["age"],
            "unique": 0,
        },
    ]

    # Convert list of dicts to list of tuples of items for easier comparison if order is not guaranteed
    # For now, direct comparison with pop should work if the number of indexes is small and fixed.

    found_indexes_simplified = []
    for index in indexes:
        found_indexes_simplified.append({
            "name": index["name"],
            "column_names": sorted(index["column_names"]), # Sort for consistency
            "unique": index["unique"],
            # Not including dialect_options as it can vary or be empty
        })

    expected_indexes_simplified = []
    for index in expected_indexes:
        expected_indexes_simplified.append({
            "name": index["name"],
            "column_names": sorted(index["column_names"]),
            "unique": index["unique"],
        })

    for expected_index in expected_indexes_simplified:
        assert expected_index in found_indexes_simplified, f"Expected index {expected_index['name']} not found or mismatch."

    assert len(found_indexes_simplified) == len(expected_indexes_simplified), \
        f"Mismatch in number of indexes. Found: {len(found_indexes_simplified)}, Expected: {len(expected_indexes_simplified)}"
