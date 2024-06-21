from unittest.mock import patch

import pytest
from sqlalchemy.exc import SAWarning
from sqlmodel import create_engine

from ....conftest import get_testing_print_function

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
        {"id": 3, "name": "Wakaland", "headquarters": "Wakaland Capital City"},
    ],
    [
        "Deleted hero:",
        None,
    ],
    [
        "Deleted hero:",
        None,
    ],
]


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.delete_records_relationship import (
        tutorial001 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        with pytest.warns(SAWarning):
            mod.main()
    assert calls == expected_calls
