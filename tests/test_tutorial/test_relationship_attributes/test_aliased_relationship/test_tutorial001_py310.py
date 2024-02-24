from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function, needs_py310

expected_calls = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "summer_team_id": 2,
            "winter_team_id": 1,
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "summer_team_id": 1,
            "winter_team_id": 1,
        },
    ],
    [
        "Heros with Preventers as their winter team:",
        [
            {
                "age": None,
                "id": 1,
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "summer_team_id": 2,
                "winter_team_id": 1,
            },
            {
                "age": 48,
                "id": 2,
                "name": "Rusty-Man",
                "secret_name": "Tommy Sharp",
                "summer_team_id": 1,
                "winter_team_id": 1,
            },
        ],
    ],
    [
        "Heros with Preventers as their winter and Z-Force as their summer team:",
        [
            {
                "age": None,
                "id": 1,
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "summer_team_id": 2,
                "winter_team_id": 1,
            }
        ],
    ],
]


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.aliased_relationship import (
        tutorial001_py310 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
