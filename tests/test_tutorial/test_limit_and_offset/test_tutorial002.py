from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function

expected_calls = [
    [
        [
            {
                "id": 4,
                "name": "Tarantula",
                "secret_name": "Natalia Roman-on",
                "age": 32,
            },
            {"id": 5, "name": "Black Lion", "secret_name": "Trevor Challa", "age": 35},
            {"id": 6, "name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36},
        ]
    ]
]


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.offset_and_limit import tutorial002 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
