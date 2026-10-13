import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine, inspect
from sqlalchemy.engine.reflection import Inspector

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial002_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.indexes.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == [
        [{"name": "Tarantula", "secret_name": "Natalia Roman-on", "age": 32, "id": 4}],
        [{"name": "Black Lion", "secret_name": "Trevor Challa", "age": 35, "id": 5}],
    ]

    insp: Inspector = inspect(mod.engine)
    indexes = insp.get_indexes(str(mod.Hero.__tablename__))
    assert {
        index["name"]: (index["column_names"], index["unique"]) for index in indexes
    } == {
        "ix_hero_name": (["name"], False),
        "ix_hero_age": (["age"], False),
    }
