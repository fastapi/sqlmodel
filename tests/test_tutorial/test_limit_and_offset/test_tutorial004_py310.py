from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_py310


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.offset_and_limit import tutorial004_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == [
        [
            [
                {"name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36, "id": 6},
                {"name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48, "id": 3},
            ]
        ]
    ]
