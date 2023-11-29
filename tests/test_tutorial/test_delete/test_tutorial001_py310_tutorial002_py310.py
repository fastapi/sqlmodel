from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Hero 1:",
        {"id": 2, "name": "Spider-Boy", "secret_name": "Pedro Parqueador", "age": None},
    ],
    [
        "Hero 2:",
        {
            "id": 7,
            "name": "Captain North America",
            "secret_name": "Esteban Rogelios",
            "age": 93,
        },
    ],
    [
        "Updated hero 1:",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    [
        "Updated hero 2:",
        {
            "id": 7,
            "name": "Captain North America Except Canada",
            "secret_name": "Esteban Rogelios",
            "age": 110,
        },
    ],
    [
        "Hero: ",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    [
        "Deleted hero:",
        {
            "id": 2,
            "name": "Spider-Youngster",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
    ["There's no hero named Spider-Youngster"],
]


@needs_py310
def test_tutorial001(clear_sqlmodel):
    from docs_src.tutorial.delete import tutorial001_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls


@needs_py310
def test_tutorial002(clear_sqlmodel):
    from docs_src.tutorial.delete import tutorial002_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
