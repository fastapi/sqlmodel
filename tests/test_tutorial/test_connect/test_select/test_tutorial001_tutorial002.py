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
        "Hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 2,
            "name": "Deadpond",
        },
        "Team:",
        {"id": 2, "name": "Z-Force", "headquarters": "Sister Margaret's Bar"},
    ],
    [
        "Hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 1,
            "name": "Rusty-Man",
        },
        "Team:",
        {"id": 1, "name": "Preventers", "headquarters": "Sharp Tower"},
    ],
]


@pytest.fixture(name="module")
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(
        f"docs_src.tutorial.connect.select.{request.param}"
    )
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    return module


@pytest.mark.parametrize(
    "module",
    [
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial001(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls


@pytest.mark.parametrize(
    "module",
    [
        "tutorial002_py39",
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial002(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls
