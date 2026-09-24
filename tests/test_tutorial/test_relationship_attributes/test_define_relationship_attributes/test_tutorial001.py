import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine

from ....conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(
        f"docs_src.tutorial.relationship_attributes.define_relationship_attributes.{request.param}"
    )
    mod.engine = database_engine
    return mod


expected_calls = [
    [
        "Created hero:",
        {
            "name": "Deadpond",
            "age": None,
            "team_id": 1,
            "id": 1,
            "secret_name": "Dive Wilson",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Rusty-Man",
            "age": 48,
            "team_id": 2,
            "id": 2,
            "secret_name": "Tommy Sharp",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Spider-Boy",
            "age": None,
            "team_id": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
        },
    ],
]


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.main()
    assert print_mock.calls == expected_calls
