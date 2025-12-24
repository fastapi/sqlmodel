import importlib
from types import ModuleType

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ...conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial002_py39",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(
        f"docs_src.tutorial.create_db_and_table.{request.param}"
    )
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    return module


def test_create_db_and_table(module: ModuleType):
    module.create_db_and_tables()
    insp: Inspector = inspect(module.engine)
    assert insp.has_table(str(module.Hero.__tablename__))
