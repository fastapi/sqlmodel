import importlib

import pytest
from dirty_equals import IsUUID
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest):
    module_name = request.param
    return importlib.import_module(f"docs_src.advanced.uuid.{module_name}")


def test_tutorial(print_mock: PrintMock, module: type) -> None:
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)

    module.main()

    # Extract UUIDs from actual calls recorded by print_mock
    first_uuid = print_mock.calls[1][0]["id"]
    assert first_uuid == IsUUID(4)

    second_uuid = print_mock.calls[7][0]["id"]
    assert second_uuid == IsUUID(4)

    assert first_uuid != second_uuid

    # Construct expected_calls using the extracted UUIDs
    expected_calls = [
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
    assert print_mock.calls == expected_calls
