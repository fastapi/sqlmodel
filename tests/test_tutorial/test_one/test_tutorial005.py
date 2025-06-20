import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound # Keep this import
from sqlmodel import create_engine, SQLModel, Session, delete # Ensure Session and delete

from ...conftest import get_testing_print_function, needs_py310, PrintMock


expected_calls_tutorial005 = [
    [
        "Hero:",
        {
            "id": 1,
            "name": "Test Hero",
            "secret_name": "Secret Test Hero",
            "age": 24,
        },
    ]
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial005",
        pytest.param("tutorial005_py310", marks=needs_py310),
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

    # Table creation logic:
    # tutorial005.py's main() attempts to select a hero, expecting NoResultFound.
    # This implies the table should exist but be empty initially for that part of main().
    # The create_db_and_tables() is called inside main() *after* the select that fails.
    # So, the fixture should create tables.
    if hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
         mod.SQLModel.metadata.create_all(mod.engine) # Create tables

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    # module.main() in tutorial005.py is structured to:
    # 1. Try selecting a hero (expects NoResultFound).
    # 2. Call create_db_and_tables().
    # 3. Create a hero (this part is commented out in docs_src, but the test does it).
    # The test then separately calls select_heroes().

    # Phase 1: Test the NoResultFound part of main()
    # The fixture already created tables, so main() trying to select might not fail with NoResultFound
    # if create_db_and_tables() in main also populates.
    # However, the original test has main() raise NoResultFound. This implies main() itself
    # first tries a select on potentially empty (but existing) tables.
    # The `clear_sqlmodel` fixture ensures the DB is clean (tables might be recreated by module_fixture).

    with pytest.raises(NoResultFound):
        module.main() # This should execute the part of main() that expects no results

    # Phase 2: Test select_heroes() after manually adding a hero
    # This part matches the original test's logic after the expected exception.
    with Session(module.engine) as session:
        session.exec(delete(module.Hero)) # Clear any heroes if main() somehow added them
        session.add(module.Hero(name="Test Hero", secret_name="Secret Test Hero", age=24))
        session.commit()

    with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
        module.select_heroes() # This function is defined in the tutorial module

    assert print_mock.calls == expected_calls_tutorial005
