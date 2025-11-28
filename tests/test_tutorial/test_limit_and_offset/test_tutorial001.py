import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine  # Added SQLModel for table creation

from ...conftest import PrintMock, get_testing_print_function, needs_py310

expected_calls_tutorial001 = [  # Renamed to be specific
    [
        [
            {"id": 1, "name": "Deadpond", "secret_name": "Dive Wilson", "age": None},
            {
                "id": 2,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "age": None,
            },
            {"id": 3, "name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48},
        ]
    ]
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def module_fixture(
    request: pytest.FixtureRequest, clear_sqlmodel: Any
):  # Changed name for clarity
    module_name = request.param
    # Corrected module path
    full_module_name = f"docs_src.tutorial.offset_and_limit.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    # Ensure tables are created. These tutorials often have create_db_and_tables() or similar in main().
    # If not, this is a safeguard.
    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
        # This function should ideally call SQLModel.metadata.create_all(engine)
        pass  # Assuming main() will call it or tables are created before select
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    # clear_sqlmodel is used by the module_fixture implicitly if needed,
    # and ensures clean DB state for the test.

    # The main function in the tutorial module typically contains the core logic,
    # including table creation (often via a helper like create_db_and_tables)
    # and the print statements we are capturing.
    # The module_fixture ensures the engine is set.
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == expected_calls_tutorial001
