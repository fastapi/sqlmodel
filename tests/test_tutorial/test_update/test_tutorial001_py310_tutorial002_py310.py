from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Hero:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ],
    [
        "Updated hero:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
]


@needs_py310
def test_tutorial001(clear_sqlmodel):
    from docs_src.tutorial.update import tutorial001_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls


@needs_py310
def test_tutorial002(clear_sqlmodel):
    from docs_src.tutorial.update import tutorial002_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
