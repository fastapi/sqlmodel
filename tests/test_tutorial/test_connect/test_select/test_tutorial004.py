import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ....conftest import PrintMock, needs_py310

expected_calls = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 2,
            "name": "Deadpond",
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 1,
            "name": "Rusty-Man",
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "name": "Spider-Boy",
        },
    ],
    [
        "Preventer Hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 1,
            "name": "Rusty-Man",
        },
    ],
]


@pytest.fixture(
    name="module",
    params=[
        "tutorial004",
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module_name = request.param
    mod = importlib.import_module(f"docs_src.tutorial.connect.select.{module_name}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(print_mock: PrintMock, module: ModuleType) -> None:
    module.main()
    assert print_mock.calls == expected_calls
