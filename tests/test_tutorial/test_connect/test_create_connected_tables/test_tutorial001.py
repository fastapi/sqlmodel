import importlib
from types import ModuleType

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ....conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module_name = request.param
    mod = importlib.import_module(
        f"docs_src.tutorial.connect.create_tables.{module_name}"
    )
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(module: ModuleType) -> None:
    module.main()
    insp: Inspector = inspect(module.engine)
    assert insp.has_table(str(module.Hero.__tablename__))
    assert insp.has_table(str(module.Team.__tablename__))
