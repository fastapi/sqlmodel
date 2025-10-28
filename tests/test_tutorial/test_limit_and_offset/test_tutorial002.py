import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, get_testing_print_function, needs_py310

expected_calls_tutorial002 = [  # Renamed for specificity
    [
        [
            {
                "id": 4,
                "name": "Tarantula",
                "secret_name": "Natalia Roman-on",
                "age": 32,
            },
            {"id": 5, "name": "Black Lion", "secret_name": "Trevor Challa", "age": 35},
            {"id": 6, "name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36},
        ]
    ]
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial002",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.offset_and_limit.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
        pass  # Assuming main() calls it
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.main()

    assert print_mock.calls == expected_calls_tutorial002
