import importlib
from dataclasses import dataclass
from types import ModuleType

import pytest
from sqlmodel import create_engine

from tests.conftest import PrintMock, needs_py310

expected_calls = [
    [
        "Created hero:",
        {
            "id": 1,
            "name": "Deadpond",
            "age": None,
            "secret_name": "Dive Wilson",
            "team_id": 1,
        },
    ],
    [
        "Hero's team:",
        {"name": "Z-Force", "headquarters": "Sister Margaret's Bar", "id": 1},
    ],
]


@dataclass
class Modules:
    app: ModuleType
    database: ModuleType


@pytest.fixture(
    name="modules",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_modules(request: pytest.FixtureRequest) -> Modules:
    app_module = importlib.import_module(
        f"docs_src.tutorial.code_structure.{request.param}.app"
    )
    database_module = importlib.import_module(
        f"docs_src.tutorial.code_structure.{request.param}.database"
    )
    database_module.sqlite_url = "sqlite://"
    database_module.engine = create_engine(database_module.sqlite_url)
    app_module.engine = database_module.engine

    return Modules(app=app_module, database=database_module)


def test_tutorial(print_mock: PrintMock, modules: Modules):
    modules.app.main()
    assert print_mock.calls == expected_calls
