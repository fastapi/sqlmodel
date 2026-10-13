import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial004_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.offset_and_limit.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert len(print_mock.calls) == 1
    assert len(print_mock.calls[0]) == 1
    heroes = print_mock.calls[0][0]
    assert len(heroes) == 2
    assert len({hero["id"] for hero in heroes}) == 2
    # Without ORDER BY, the database determines which matching heroes are returned.
    expected_heroes = [
        {"name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48, "id": 3},
        {"name": "Black Lion", "secret_name": "Trevor Challa", "age": 35, "id": 5},
        {"name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36, "id": 6},
        {
            "name": "Captain North America",
            "secret_name": "Esteban Rogelios",
            "age": 93,
            "id": 7,
        },
    ]
    for hero in heroes:
        assert hero in expected_heroes
