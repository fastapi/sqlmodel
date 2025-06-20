import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine, SQLModel

from ...conftest import get_testing_print_function, needs_py310, PrintMock


# expected_calls is defined within the test_tutorial function in the original test


@pytest.fixture(
    name="module",
    params=[
        "tutorial004",
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.where.{module_name}"

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

    expected_calls = [
        [{"id": 5, "name": "Black Lion", "secret_name": "Trevor Challa", "age": 35}],
        [{"id": 6, "name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36}],
        [{"id": 3, "name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48}],
        [
            {
                "id": 7,
                "name": "Captain North America",
                "secret_name": "Esteban Rogelios",
                "age": 93,
            }
        ],
    ]
    # Preserve the original assertion logic
    for call_item in expected_calls:
        assert call_item in print_mock.calls, "This expected item should be in the list"
        print_mock.calls.pop(print_mock.calls.index(call_item))
    assert len(print_mock.calls) == 0, "The list should only have the expected items"
