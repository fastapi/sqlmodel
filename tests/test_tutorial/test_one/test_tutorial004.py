import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy.exc import MultipleResultsFound  # Keep this import
from sqlmodel import (  # Ensure Session and delete are imported
    Session,
    create_engine,
    delete,
)

from ...conftest import PrintMock, get_testing_print_function, needs_py310

expected_calls_tutorial004 = [
    [
        "Hero:",
        {
            "id": 1,  # Assuming ID will be 1 after clearing and adding one hero
            "name": "Test Hero",
            "secret_name": "Secret Test Hero",
            "age": 24,
        },
    ]
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial004",
        pytest.param("tutorial004_py310", marks=needs_py310),
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

    # Table creation is crucial here because the test interacts with the DB
    # before calling main() in some cases (to clean up, then assert specific state).
    # The main() function in tutorial004.py is expected to cause MultipleResultsFound,
    # which implies tables and data should exist *before* main() is called for that specific check.
    # The original test calls main() first, then manipulates DB.
    # The fixture should ensure tables are ready.
    if hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    # The module.main() in tutorial004.py is designed to initially create heroes,
    # then try to select one which results in MultipleResultsFound.
    # It also defines select_heroes() which is called later.

    # First, let main() run to create initial data and trigger the expected exception.
    # The create_db_and_tables is called within main() in docs_src/tutorial/one/tutorial004.py
    with pytest.raises(MultipleResultsFound):
        module.main()  # This function in the tutorial is expected to raise this

    # After the expected exception, the original test clears the Hero table and adds a specific hero.
    with Session(module.engine) as session:
        # The delete statement needs the actual Hero class from the module
        session.exec(delete(module.Hero))
        session.add(
            module.Hero(name="Test Hero", secret_name="Secret Test Hero", age=24)
        )
        session.commit()

    # Now, test the select_heroes function part
    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.select_heroes()  # This function is defined in the tutorial module

    assert print_mock.calls == expected_calls_tutorial004
