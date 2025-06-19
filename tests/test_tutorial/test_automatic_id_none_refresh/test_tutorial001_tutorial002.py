import importlib
from types import ModuleType
from typing import Any, Dict, List, Union

import pytest
from sqlmodel import create_engine

from tests.conftest import PrintMock, needs_py310


def check_calls(calls: List[List[Union[str, Dict[str, Any]]]]) -> None:
    assert calls[0] == ["Before interacting with the database"]
    assert calls[1] == [
        "Hero 1:",
        {
            "id": None,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
        },
    ]
    assert calls[2] == [
        "Hero 2:",
        {
            "id": None,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ]
    assert calls[3] == [
        "Hero 3:",
        {
            "id": None,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        },
    ]
    assert calls[4] == ["After adding to the session"]
    assert calls[5] == [
        "Hero 1:",
        {
            "id": None,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
        },
    ]
    assert calls[6] == [
        "Hero 2:",
        {
            "id": None,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ]
    assert calls[7] == [
        "Hero 3:",
        {
            "id": None,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        },
    ]
    assert calls[8] == ["After committing the session"]
    assert calls[9] == ["Hero 1:", {}]
    assert calls[10] == ["Hero 2:", {}]
    assert calls[11] == ["Hero 3:", {}]
    assert calls[12] == ["After committing the session, show IDs"]
    assert calls[13] == ["Hero 1 ID:", 1]
    assert calls[14] == ["Hero 2 ID:", 2]
    assert calls[15] == ["Hero 3 ID:", 3]
    assert calls[16] == ["After committing the session, show names"]
    assert calls[17] == ["Hero 1 name:", "Deadpond"]
    assert calls[18] == ["Hero 2 name:", "Spider-Boy"]
    assert calls[19] == ["Hero 3 name:", "Rusty-Man"]
    assert calls[20] == ["After refreshing the heroes"]
    assert calls[21] == [
        "Hero 1:",
        {
            "id": 1,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
        },
    ]
    assert calls[22] == [
        "Hero 2:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ]
    assert calls[23] == [
        "Hero 3:",
        {
            "id": 3,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        },
    ]
    assert calls[24] == ["After the session closes"]
    assert calls[21] == [
        "Hero 1:",
        {
            "id": 1,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
        },
    ]
    assert calls[22] == [
        "Hero 2:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ]
    assert calls[23] == [
        "Hero 3:",
        {
            "id": 3,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        },
    ]


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        "tutorial002",
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(
        f"docs_src.tutorial.automatic_id_none_refresh.{request.param}"
    )
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)

    return module


def test_tutorial_001_tutorial_002(print_mock: PrintMock, module: ModuleType) -> None:
    module.main()
    check_calls(print_mock.calls)
