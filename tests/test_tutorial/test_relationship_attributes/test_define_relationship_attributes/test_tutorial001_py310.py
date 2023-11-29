from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Created hero:",
        {
            "name": "Deadpond",
            "age": None,
            "team_id": 1,
            "id": 1,
            "secret_name": "Dive Wilson",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Rusty-Man",
            "age": 48,
            "team_id": 2,
            "id": 2,
            "secret_name": "Tommy Sharp",
        },
    ],
    [
        "Created hero:",
        {
            "name": "Spider-Boy",
            "age": None,
            "team_id": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
        },
    ],
]


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.define_relationship_attributes import (
        tutorial001_py310 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
