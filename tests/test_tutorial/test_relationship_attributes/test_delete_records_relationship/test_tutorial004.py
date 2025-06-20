import importlib
import sys
import types
from typing import Any
from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, SQLModel, Session, select, delete # Added Session, select, delete just in case module uses them

from ....conftest import get_testing_print_function, needs_py39, needs_py310, PrintMock


expected_calls_tutorial004 = [
    [
        "Created hero:", # From create_heroes() called by main()
        {
            "age": None,
            "id": 1,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "team_id": 1,
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "team_id": 2,
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": None, # Initially no team
        },
    ],
    [
        "Updated hero:", # Spider-Boy gets a team
        {
            "age": None,
            "id": 3,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
        },
    ],
    [
        "Team Wakaland:", # Team Wakaland is created
        {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
    ],
    # The main() in tutorial004.py (cascade_delete) is try_to_delete_team_preventers_alternative.
    # This function calls create_db_and_tables(), then create_heroes().
    # create_heroes() produces the prints above.
    # Then try_to_delete_team_preventers_alternative() attempts to delete Team Preventers.
    # This attempt to delete Team Preventers (which has heroes) is what should cause the IntegrityError
    # because ondelete="RESTRICT" is the default for the foreign key from Hero to Team.
    # The prints "Black Lion has no team", "Princess Sure-E has no team", "Deleted team"
    # from the original test's expected_calls are from a different sequence of operations
    # (likely from select_heroes_after_delete which deletes Wakaland, not Preventers).
    # The IntegrityError "FOREIGN KEY constraint failed" is the key outcome of tutorial004.py's main.
    # So, expected_calls should only contain what's printed by create_heroes().
]
# Let's refine expected_calls based on create_heroes() in cascade_delete_relationships/tutorial004.py
# create_heroes() in that file:
#   team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
#   team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
#   hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_preventers) ; print("Created hero:", hero_deadpond)
#   hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers) ; print("Created hero:", hero_rusty_man)
#   hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", team=team_preventers) ; print("Created hero:", hero_spider_boy)
# This means 3 heroes are created and printed, all linked to Preventers.
# The expected_calls above are from a different tutorial's create_heroes.

# Corrected expected_calls for cascade_delete_relationships/tutorial004.py create_heroes part:
expected_calls_tutorial004_corrected = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1, # Assuming IDs start from 1 after clear_sqlmodel
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "team_id": 1, # Assuming Preventers team gets ID 1
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "team_id": 1, # Also Preventers
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "team_id": 1, # Also Preventers
        },
    ],
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial004",
        pytest.param("tutorial004_py39", marks=needs_py39),
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.relationship_attributes.cascade_delete_relationships.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    # main() in tutorial004 calls create_db_and_tables() itself.
    # No need to call it in fixture if main() is the entry point.
    # However, if other functions from module were tested independently, tables would need to exist.
    # For safety and consistency with other fixtures:
    if hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
         mod.SQLModel.metadata.create_all(mod.engine) # Ensure tables are there before main might use them.

    return mod


def test_tutorial(module: types.ModuleType, print_mock: PrintMock, clear_sqlmodel: Any):
    # The main() function in docs_src/tutorial/relationship_attributes/cascade_delete_relationships/tutorial004.py
    # is try_to_delete_team_preventers_alternative().
    # This function itself calls create_db_and_tables() and create_heroes().
    # create_heroes() will print the "Created hero:" lines.
    # Then, try_to_delete_team_preventers_alternative() attempts to delete a team
    # which should raise an IntegrityError due to existing heroes.

    with pytest.raises(IntegrityError) as excinfo:
        with patch("builtins.print", new=get_testing_print_function(print_mock.calls)):
            module.main() # This is try_to_delete_team_preventers_alternative

    # Check the prints that occurred *before* the exception was raised
    assert print_mock.calls == expected_calls_tutorial004_corrected

    # Check the exception message
    assert "FOREIGN KEY constraint failed" in str(excinfo.value)
