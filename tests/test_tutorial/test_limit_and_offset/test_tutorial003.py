import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.offset_and_limit.{request.param}")
    mod.engine = database_engine
    return mod


expected_calls = [
    [
        [
            {
                "id": 7,
                "name": "Captain North America",
                "secret_name": "Esteban Rogelios",
                "age": 93,
            }
        ]
    ]
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
