import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, get_testing_print_function, needs_py310

expected_calls_tutorial007 = [
    [
        "Hero:",
        {"name": "Deadpond", "secret_name": "Dive Wilson", "age": None, "id": 1},
    ]
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial007",
        pytest.param("tutorial007_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.one.{module_name}"

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

    assert print_mock.calls == expected_calls_tutorial007
