import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial006_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.one.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == [
        [
            "Hero:",
            {"name": "Deadpond", "secret_name": "Dive Wilson", "age": None, "id": 1},
        ]
    ]
