from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.cascade_delete_relationships import (
        tutorial001 as mod,
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
            {"name": "Wakaland", "id": 3, "headquarters": "Wakaland Capital City"},
        ],
        [
            "Deleted team:",
            {"name": "Wakaland", "id": 3, "headquarters": "Wakaland Capital City"},
        ],
        ["Black Lion not found:", None],
        ["Princess Sure-E not found:", None],
    ]
