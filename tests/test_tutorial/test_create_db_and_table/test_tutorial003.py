import importlib
from types import ModuleType
from typing import Any  # For clear_sqlmodel type hint

import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ...conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module_name = request.param
    mod = importlib.import_module(
        f"docs_src.tutorial.create_db_and_table.{module_name}"
    )
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_create_db_and_table(clear_sqlmodel: Any, module: ModuleType) -> None:
    module.create_db_and_tables()
    insp: Inspector = inspect(module.engine)
    assert insp.has_table(str(module.Hero.__tablename__))
