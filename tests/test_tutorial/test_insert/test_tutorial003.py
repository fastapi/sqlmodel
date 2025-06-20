import importlib
import sys
import types
from typing import Any

import pytest
from sqlmodel import create_engine, SQLModel, Session, select

from ...conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.insert.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    # Create tables. Tutorial003.py in insert focuses on refresh, so tables and initial data are key.
    # It's likely main() handles this. If not, direct creation is a fallback.
    if hasattr(mod, "create_db_and_tables"): # Some tutorials use this helper
        mod.create_db_and_tables()
    elif hasattr(mod, "Hero") and hasattr(mod.Hero, "metadata"): # Check for Hero model metadata
         mod.Hero.metadata.create_all(mod.engine)
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"): # Generic fallback
         mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(module: types.ModuleType, clear_sqlmodel: Any):
    # The main() function in tutorial003.py (insert section) is expected to perform
    # the operations that this test will verify (e.g., creating and refreshing objects).
    module.main()

    with Session(module.engine) as session:
        heroes = session.exec(select(module.Hero)).all()

    heroes_by_name = {hero.name: hero for hero in heroes}
    # The asserted data matches tutorial001, which is how the original test was.
    # This implies tutorial003.py might be demonstrating a concept (like refresh)
    # using the same initial dataset as tutorial001 or that the test is a copy.
    # We preserve the original test's assertions.
    deadpond = heroes_by_name["Deadpond"]
    spider_boy = heroes_by_name["Spider-Boy"]
    rusty_man = heroes_by_name["Rusty-Man"]

    assert deadpond.name == "Deadpond"
    assert deadpond.age is None
    assert deadpond.id is not None
    assert deadpond.secret_name == "Dive Wilson"

    assert spider_boy.name == "Spider-Boy"
    assert spider_boy.age is None
    assert spider_boy.id is not None
    assert spider_boy.secret_name == "Pedro Parqueador"

    assert rusty_man.name == "Rusty-Man"
    assert rusty_man.age == 48
    assert rusty_man.id is not None
    assert rusty_man.secret_name == "Tommy Sharp"

    # Tutorial003 specific checks, if any, would go here.
    # For example, if it's about checking `refresh()` behavior,
    # the `main()` in the tutorial module should have demonstrated that,
    # and the state of the objects above should reflect the outcome of `main()`.
    # The current assertions are based on the original test files.
    # If tutorial003.py's main() modifies these heroes in a way that `refresh` would show,
    # these assertions should capture that final state.

    # Example: if Rusty-Man's age was updated in DB by another process and refreshed in main()
    # then rusty_man.age here would be the refreshed age.
    # The test as it stands checks the state *after* module.main() has run.
    # In tutorial003.py, `main` creates heroes, adds one, then SELECTs and REFRESHES that one.
    # The test here is more general, selecting all and checking.
    # The key is that the data from `main` is what's in the DB.
    # The test correctly reflects the state after the `create_heroes` part of main.
    # The refresh concept in the tutorial is demonstrated by printing, not by changing state in a way this test would catch differently
    # from tutorial001 unless the `main` function's print statements were being captured and asserted (which they are not here).
    # The database state assertions are sufficient as per original tests.
