import importlib
from types import ModuleType

import pytest
from dirty_equals import IsUUID
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.advanced.uuid.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    mod.main()
    first_uuid = print_mock.calls[1][0]["id"]
    assert first_uuid == IsUUID(4)

    second_uuid = print_mock.calls[7][0]["id"]
    assert second_uuid == IsUUID(4)

    assert first_uuid != second_uuid

    assert print_mock.calls == [
        ["The hero before saving in the DB"],
        [
            {
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "id": first_uuid,
                "age": None,
            }
        ],
        ["The hero ID was already set"],
        [first_uuid],
        ["After saving in the DB"],
        [
            {
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "age": None,
                "id": first_uuid,
            }
        ],
        ["Created hero:"],
        [
            {
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "age": None,
                "id": second_uuid,
            }
        ],
        ["Created hero ID:"],
        [second_uuid],
        ["Selected hero:"],
        [
            {
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "age": None,
                "id": second_uuid,
            }
        ],
        ["Selected hero ID:"],
        [second_uuid],
    ]
