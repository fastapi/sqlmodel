from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Deadpond:",
        {"id": 1, "secret_name": "Dive Wilson", "age": None, "name": "Deadpond"},
    ],
    [
        "Deadpond teams:",
        [
            {"id": 1, "name": "Z-Force", "headquarters": "Sister Margaret's Bar"},
            {"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"},
        ],
    ],
    [
        "Rusty-Man:",
        {"id": 2, "secret_name": "Tommy Sharp", "age": 48, "name": "Rusty-Man"},
    ],
    [
        "Rusty-Man Teams:",
        [{"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"}],
    ],
    [
        "Spider-Boy:",
        {"id": 3, "secret_name": "Pedro Parqueador", "age": None, "name": "Spider-Boy"},
    ],
    [
        "Spider-Boy Teams:",
        [{"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"}],
    ],
]


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.many_to_many import tutorial001_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
