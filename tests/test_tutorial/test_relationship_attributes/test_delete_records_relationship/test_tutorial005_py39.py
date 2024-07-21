from unittest.mock import patch

from sqlmodel import create_engine

from tests.conftest import get_testing_print_function, needs_py39


@needs_py39
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.cascade_delete_relationships import (
        tutorial005_py39 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == [
        [
            "Created hero:",
            {
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "team_id": 1,
                "id": 1,
                "age": None,
            },
        ],
        [
            "Created hero:",
            {
                "name": "Rusty-Man",
                "secret_name": "Tommy Sharp",
                "team_id": 2,
                "id": 2,
                "age": 48,
            },
        ],
        [
            "Created hero:",
            {
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": None,
                "id": 3,
                "age": None,
            },
        ],
        [
            "Updated hero:",
            {
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": 2,
                "id": 3,
                "age": None,
            },
        ],
        [
            "Team Wakaland:",
            {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
        ],
        [
            "Team with removed heroes:",
            {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
        ],
        [
            "Deleted team:",
            {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
        ],
        [
            "Black Lion has no team:",
            {
                "name": "Black Lion",
                "secret_name": "Trevor Challa",
                "team_id": None,
                "id": 4,
                "age": 35,
            },
        ],
        [
            "Princess Sure-E has no team:",
            {
                "name": "Princess Sure-E",
                "secret_name": "Sure-E",
                "team_id": None,
                "id": 5,
                "age": None,
            },
        ],
    ]
