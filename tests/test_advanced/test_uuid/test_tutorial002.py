from unittest.mock import patch

from dirty_equals import IsUUID
from sqlmodel import create_engine

from ...conftest import get_testing_print_function


def test_tutorial(clear_sqlmodel) -> None:
    from docs_src.advanced.uuid import tutorial002 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    first_uuid = calls[1][0]["id"]
    assert first_uuid == IsUUID(4)

    second_uuid = calls[7][0]["id"]
    assert second_uuid == IsUUID(4)

    assert first_uuid != second_uuid

    assert calls == [
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
