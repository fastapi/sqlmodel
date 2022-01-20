from decimal import Decimal
from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function

expected_calls = [
    [
        "Hero 1:",
        {
            "name": "Deadpond",
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "money": Decimal("1.100"),
        },
    ],
    [
        "Hero 2:",
        {
            "name": "Rusty-Man",
            "age": 48,
            "id": 3,
            "secret_name": "Tommy Sharp",
            "money": Decimal("2.200"),
        },
    ],
    ["Total money: 3.300"],
]


def test_tutorial(clear_sqlmodel):
    from docs_src.advanced.decimal import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
