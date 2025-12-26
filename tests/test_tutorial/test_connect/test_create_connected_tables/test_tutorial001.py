import importlib
from types import ModuleType

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from tests.conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(
        f"docs_src.tutorial.connect.create_tables.{request.param}"
    )
    return module


def test_tutorial001(module: ModuleType):
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    module.main()
    insp: Inspector = inspect(module.engine)
    assert insp.has_table(str(module.Hero.__tablename__))
    assert insp.has_table(str(module.Team.__tablename__))
