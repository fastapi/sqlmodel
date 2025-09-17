import importlib
import sys
import types
from typing import Any

import pytest
from sqlmodel import (  # Ensure all necessary SQLModel parts are imported
    Session,
    create_engine,
    select,
)

from ...conftest import needs_py310  # Adjusted for typical conftest location


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.insert.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"  # Ensure this is consistent
    mod.engine = create_engine(mod.sqlite_url)  # Standard engine setup

    # Table creation is usually in main() for these examples or implicitly by SQLModel.metadata.create_all
    # If main() creates tables, calling it here might be redundant if test_tutorial also calls it.
    # For safety, ensure tables are created if Hero model is defined directly in the module.
    if hasattr(mod, "Hero") and hasattr(mod.Hero, "metadata"):
        mod.Hero.metadata.create_all(mod.engine)
    elif hasattr(mod, "SQLModel") and hasattr(mod.SQLModel, "metadata"):
        mod.SQLModel.metadata.create_all(mod.engine)

    return mod


def test_tutorial(
    module: types.ModuleType, clear_sqlmodel: Any
):  # clear_sqlmodel still useful for DB state
    # If module.main() is responsible for creating data and potentially tables, call it.
    # The fixture get_module now ensures the engine is set and tables are created if models are defined.
    # If main() also sets up engine/tables, ensure it's idempotent or adjust.
    # Typically, main() in these tutorials contains the primary logic to be tested (e.g., data insertion).
    module.main()  # This should execute the tutorial's data insertion logic

    with Session(module.engine) as session:
        heroes = session.exec(select(module.Hero)).all()

    heroes_by_name = {hero.name: hero for hero in heroes}
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
