import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine, SQLModel # Added SQLModel

from ...conftest import get_testing_print_function, needs_py310, PrintMock


@pytest.fixture(
    name="module",
    params=[
        "tutorial002",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.indexes.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    if hasattr(mod, "Hero") and hasattr(mod.Hero, "metadata"):
         mod.Hero.metadata.create_all(mod.engine)
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
         mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(print_mock: PrintMock, module: types.ModuleType):
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == [
        [{"name": "Tarantula", "secret_name": "Natalia Roman-on", "age": 32, "id": 4}],
        [{"name": "Black Lion", "secret_name": "Trevor Challa", "age": 35, "id": 5}],
    ]

    insp: Inspector = inspect(module.engine)
    table_name = str(module.Hero.__tablename__)
    indexes = insp.get_indexes(table_name)

    expected_indexes = [
        {
            "name": "ix_hero_name",
            "dialect_options": {}, # Included for completeness but not strictly compared below
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

    found_indexes_simplified = []
    for index in indexes:
        found_indexes_simplified.append({
            "name": index["name"],
            "column_names": sorted(index["column_names"]),
            "unique": index["unique"],
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
