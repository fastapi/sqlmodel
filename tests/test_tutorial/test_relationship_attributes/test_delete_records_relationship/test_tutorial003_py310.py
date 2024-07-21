from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function, needs_py310


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.cascade_delete_relationships import (
        tutorial003_py310 as mod,
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
                "age": None,
                "id": 1,
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "team_id": 1,
            },
        ],
        [
            "Created hero:",
            {
                "age": 48,
                "id": 2,
                "name": "Rusty-Man",
                "secret_name": "Tommy Sharp",
                "team_id": 2,
            },
        ],
        [
            "Created hero:",
            {
                "age": None,
                "id": 3,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": None,
            },
        ],
        [
            "Updated hero:",
            {
                "age": None,
                "id": 3,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": 2,
            },
        ],
        [
            "Team Wakaland:",
            {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
        ],
        [
            "Deleted team:",
            {"id": 3, "headquarters": "Wakaland Capital City", "name": "Wakaland"},
        ],
        [
            "Black Lion has no team:",
            {
                "age": 35,
                "id": 4,
                "name": "Black Lion",
                "secret_name": "Trevor Challa",
                "team_id": None,
            },
        ],
        [
            "Princess Sure-E has no team:",
            {
                "age": None,
                "id": 5,
                "name": "Princess Sure-E",
                "secret_name": "Sure-E",
                "team_id": None,
            },
        ],
    ]
