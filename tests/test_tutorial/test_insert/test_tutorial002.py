import importlib
import sys
import types
from typing import Any

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from ...conftest import needs_py310  # Use aliased import


@pytest.fixture(
    name="module",  # Fixture provides the main module to be tested (tutorial002 variant)
    params=[
        "tutorial002",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel_fixture: Any):
    module_name_tut002 = request.param

    # Determine corresponding tutorial001 module name
    if module_name_tut002.endswith("_py310"):
        module_name_tut001 = "tutorial001_py310"
    else:
        module_name_tut001 = "tutorial001"

    full_module_name_tut002 = f"docs_src.tutorial.insert.{module_name_tut002}"
    full_module_name_tut001 = f"docs_src.tutorial.insert.{module_name_tut001}"

    # Load tutorial001 module to get the Team model definition
    # We need this so that when tutorial002's Hero model (with FK to Team) is defined,
    # SQLModel's metadata can correctly link them.
    # Reload to ensure freshness and avoid state leakage if modules were already imported.
    # clear_sqlmodel_fixture should have run, clearing global SQLModel.metadata.

    mod_tut001: types.ModuleType
    if full_module_name_tut001 in sys.modules:
        mod_tut001 = importlib.reload(sys.modules[full_module_name_tut001])
    else:
        mod_tut001 = importlib.import_module(full_module_name_tut001)

    TeamModel = mod_tut001.Team

    # Load tutorial002 module
    mod_tut002: types.ModuleType
    if full_module_name_tut002 in sys.modules:
        mod_tut002 = importlib.reload(sys.modules[full_module_name_tut002])
    else:
        mod_tut002 = importlib.import_module(full_module_name_tut002)

    # Attach TeamModel to the tutorial002 module object so it's accessible via module.Team
    # This is crucial if tutorial002.py itself doesn't do `from .tutorial001 import Team`
    # or if it does but `Team` is not an attribute for some reason.
    # This also helps SQLModel resolve the relationship when Hero is defined in tutorial002.
    mod_tut002.Team = TeamModel

    # Setup engine and create tables.
    # SQLModel.metadata should now be populated with models from both tutorial001 (Team, Hero)
    # and tutorial002 (its own Hero, which might override tutorial001.Hero if names clash
    # but SQLModel should handle this by now, or raise if it's an issue).
    # The key is that by attaching .Team, when tutorial002.Hero is processed, it finds TeamModel.
    mod_tut002.sqlite_url = "sqlite://"
    mod_tut002.engine = create_engine(mod_tut002.sqlite_url)

    # Create all tables. This should include Hero from tutorial002 and Team from tutorial001.
    # If tutorial001 also defines a Hero, there could be a clash if not handled by SQLModel's metadata.
    # The `clear_sqlmodel_fixture` should ensure metadata is fresh before this fixture runs.
    # When mod_tut001 is loaded, its models (Hero, Team) are registered.
    # When mod_tut002 is loaded, its Hero is registered.
    # If both Hero models are identical or one extends another with proper SQLAlchemy config, it's fine.
    # If they are different but map to same table name, it's an issue.
    # Given tutorial002.Hero links to tutorial001.Team, they must share metadata.
    SQLModel.metadata.create_all(mod_tut002.engine)

    return mod_tut002


def test_tutorial(
    module: types.ModuleType, clear_sqlmodel_fixture: Any
):  # `module` is tutorial002 with .Team attached
    module.main()  # Executes the tutorial002's data insertion logic

    with Session(module.engine) as session:
        hero_spider_boy = session.exec(
            select(module.Hero).where(module.Hero.name == "Spider-Boy")
        ).one()
        # module.Team should now be valid as it was attached in the fixture
        team_preventers = session.exec(
            select(module.Team).where(module.Team.name == "Preventers")
        ).one()
        assert hero_spider_boy.team_id == team_preventers.id
        assert (
            hero_spider_boy.team == team_preventers
        )  # This checks the relationship resolves

        heroes = session.exec(select(module.Hero)).all()

    heroes_by_name = {hero.name: hero for hero in heroes}
    deadpond = heroes_by_name["Deadpond"]
    spider_boy_retrieved = heroes_by_name["Spider-Boy"]
    rusty_man = heroes_by_name["Rusty-Man"]

    assert deadpond.name == "Deadpond"
    assert deadpond.age == 48
    assert deadpond.id is not None
    assert deadpond.secret_name == "Dive Wilson"

    assert spider_boy_retrieved.name == "Spider-Boy"
    assert spider_boy_retrieved.age == 16
    assert spider_boy_retrieved.id is not None
    assert spider_boy_retrieved.secret_name == "Pedro Parqueador"

    assert rusty_man.name == "Rusty-Man"
    assert rusty_man.age == 48
    assert rusty_man.id is not None
    assert rusty_man.secret_name == "Tommy Sharp"

    tarantula = heroes_by_name["Tarantula"]
    assert tarantula.name == "Tarantula"
    assert tarantula.age == 32
    assert tarantula.team_id is not None

    teams = session.exec(select(module.Team)).all()
    teams_by_name = {team.name: team for team in teams}
    assert "Preventers" in teams_by_name
    assert "Z-Force" in teams_by_name
    assert teams_by_name["Preventers"].headquarters == "Sharp Tower"
    assert teams_by_name["Z-Force"].headquarters == "Sister Margaret’s Bar"

    assert deadpond.team.name == "Preventers"
    assert spider_boy_retrieved.team.name == "Preventers"
    assert rusty_man.team.name == "Preventers"
    assert heroes_by_name["Tarantula"].team.name == "Z-Force"
    assert heroes_by_name["Dr. Weird"].team.name == "Z-Force"
    assert heroes_by_name["Captain North"].team.name == "Preventers"

    assert len(teams_by_name["Preventers"].heroes) == 4
    assert len(teams_by_name["Z-Force"].heroes) == 2
