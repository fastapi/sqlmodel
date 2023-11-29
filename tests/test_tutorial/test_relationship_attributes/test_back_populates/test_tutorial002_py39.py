from unittest.mock import patch

from sqlmodel import create_engine

from ....conftest import get_testing_print_function, needs_py39

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
        {"id": 3, "name": "Wakaland", "headquarters": "Wakaland Capital City"},
    ],
    [
        "Preventers new hero:",
        {
            "age": 32,
            "id": 6,
            "secret_name": "Natalia Roman-on",
            "team_id": 2,
            "name": "Tarantula",
        },
    ],
    [
        "Preventers new hero:",
        {
            "age": 36,
            "id": 7,
            "secret_name": "Steve Weird",
            "team_id": 2,
            "name": "Dr. Weird",
        },
    ],
    [
        "Preventers new hero:",
        {
            "age": 93,
            "id": 8,
            "secret_name": "Esteban Rogelios",
            "team_id": 2,
            "name": "Captain North America",
        },
    ],
    [
        "Preventers heroes:",
        [
            {
                "age": 48,
                "id": 2,
                "secret_name": "Tommy Sharp",
                "team_id": 2,
                "name": "Rusty-Man",
            },
            {
                "age": None,
                "id": 3,
                "secret_name": "Pedro Parqueador",
                "team_id": 2,
                "name": "Spider-Boy",
            },
            {
                "age": 32,
                "id": 6,
                "secret_name": "Natalia Roman-on",
                "team_id": 2,
                "name": "Tarantula",
            },
            {
                "age": 36,
                "id": 7,
                "secret_name": "Steve Weird",
                "team_id": 2,
                "name": "Dr. Weird",
            },
            {
                "age": 93,
                "id": 8,
                "secret_name": "Esteban Rogelios",
                "team_id": 2,
                "name": "Captain North America",
            },
        ],
    ],
    [
        "Hero Spider-Boy:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
            "name": "Spider-Boy",
        },
    ],
    [
        "Preventers Team:",
        {"id": 2, "name": "Preventers", "headquarters": "Sharp Tower"},
    ],
    [
        "Preventers Team Heroes:",
        [
            {
                "age": 48,
                "id": 2,
                "secret_name": "Tommy Sharp",
                "team_id": 2,
                "name": "Rusty-Man",
            },
            {
                "age": None,
                "id": 3,
                "secret_name": "Pedro Parqueador",
                "team_id": 2,
                "name": "Spider-Boy",
            },
            {
                "age": 32,
                "id": 6,
                "secret_name": "Natalia Roman-on",
                "team_id": 2,
                "name": "Tarantula",
            },
            {
                "age": 36,
                "id": 7,
                "secret_name": "Steve Weird",
                "team_id": 2,
                "name": "Dr. Weird",
            },
            {
                "age": 93,
                "id": 8,
                "secret_name": "Esteban Rogelios",
                "team_id": 2,
                "name": "Captain North America",
            },
        ],
    ],
    [
        "Spider-Boy without team:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": 2,
            "name": "Spider-Boy",
        },
    ],
    [
        "Preventers Team Heroes again:",
        [
            {
                "age": 48,
                "id": 2,
                "secret_name": "Tommy Sharp",
                "team_id": 2,
                "name": "Rusty-Man",
            },
            {
                "age": 32,
                "id": 6,
                "secret_name": "Natalia Roman-on",
                "team_id": 2,
                "name": "Tarantula",
            },
            {
                "age": 36,
                "id": 7,
                "secret_name": "Steve Weird",
                "team_id": 2,
                "name": "Dr. Weird",
            },
            {
                "age": 93,
                "id": 8,
                "secret_name": "Esteban Rogelios",
                "team_id": 2,
                "name": "Captain North America",
            },
        ],
    ],
    ["After committing"],
    [
        "Spider-Boy after commit:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "name": "Spider-Boy",
        },
    ],
    [
        "Preventers Team Heroes after commit:",
        [
            {
                "age": 48,
                "id": 2,
                "secret_name": "Tommy Sharp",
                "team_id": 2,
                "name": "Rusty-Man",
            },
            {
                "age": 32,
                "id": 6,
                "secret_name": "Natalia Roman-on",
                "team_id": 2,
                "name": "Tarantula",
            },
            {
                "age": 36,
                "id": 7,
                "secret_name": "Steve Weird",
                "team_id": 2,
                "name": "Dr. Weird",
            },
            {
                "age": 93,
                "id": 8,
                "secret_name": "Esteban Rogelios",
                "team_id": 2,
                "name": "Captain North America",
            },
        ],
    ],
]


@needs_py39
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.back_populates import (
        tutorial002_py39 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
