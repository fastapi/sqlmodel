from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 1,
            "name": "Deadpond",
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 2,
            "name": "Rusty-Man",
        },
    ],
    [
        "Created hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "name": "Spider-Boy",
        },
    ],
    [
        "Updated hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
            "name": "Spider-Boy",
        },
    ],
    [
        "Team Wakaland:",
        {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
    ],
    [
        "Deleted team:",
        {
            "id": 3,
            "name": "Wakaland",
            "headquarters": "Wakaland Capital City",
        },
    ],
    [
        "Black Lion hero:",
        {
            "age": 35,
            "id": 4,
            "secret_name": "Trevor Challa",
            "team_id": None,
            "name": "Black Lion",
        },
    ],
    [
        "Princess Sure-E hero:",
        {
            "age": None,
            "id": 5,
            "secret_name": "Sure-E",
            "team_id": None,
            "name": "Princess Sure-E",
        },
    ],
]


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.delete_records_relationship import (
        tutorial002_py310 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
