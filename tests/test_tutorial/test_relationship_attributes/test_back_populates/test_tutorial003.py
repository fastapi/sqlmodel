import importlib
from types import ModuleType

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ....conftest import needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(
        f"docs_src.tutorial.relationship_attributes.back_populates.{request.param}"
    )
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(mod: ModuleType):
    mod.main()
    insp: Inspector = inspect(mod.engine)
    assert insp.has_table(str(mod.Hero.__tablename__))
    assert insp.has_table(str(mod.Weapon.__tablename__))
    assert insp.has_table(str(mod.Power.__tablename__))
    assert insp.has_table(str(mod.Team.__tablename__))
