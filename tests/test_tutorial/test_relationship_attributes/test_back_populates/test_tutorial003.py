import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine, inspect
from sqlalchemy.engine.reflection import Inspector


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(
        f"docs_src.tutorial.relationship_attributes.back_populates.{request.param}"
    )
    mod.engine = database_engine
    return mod


def test_tutorial(mod: ModuleType):
    mod.main()
    insp: Inspector = inspect(mod.engine)
    assert insp.has_table(str(mod.Hero.__tablename__))
    assert insp.has_table(str(mod.Weapon.__tablename__))
    assert insp.has_table(str(mod.Power.__tablename__))
    assert insp.has_table(str(mod.Team.__tablename__))
