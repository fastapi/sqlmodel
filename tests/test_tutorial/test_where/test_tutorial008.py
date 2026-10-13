import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial008_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.where.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == [
        [{"id": 5, "name": "Black Lion", "secret_name": "Trevor Challa", "age": 35}],
        [{"id": 6, "name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36}],
    ]
