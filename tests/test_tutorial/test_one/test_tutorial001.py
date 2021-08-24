from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.one import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == [
        [
            "Hero:",
            {
                "name": "Tarantula",
                "secret_name": "Natalia Roman-on",
                "age": 32,
                "id": 4,
            },
        ]
    ]
