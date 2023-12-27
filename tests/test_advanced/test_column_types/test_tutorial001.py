from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function

expected_calls = [
    [
        "Villian 1:",
        {
            "name": "Green Gobbler",
            "country_code": "US",
        },
        500,
    ],
    [
        "Villian 2:",
        {
            "name": "Low-key",
            "country_code": "AS",
        },
        500,
    ],
]


def test_tutorial(clear_sqlmodel):
    """
    Unfortunately, SQLite does not enforce varchar lengths, so we can't test an oversize case without spinning up a
    database engine.

    """

    from docs_src.advanced.column_types import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
