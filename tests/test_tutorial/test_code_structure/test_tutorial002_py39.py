from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function, needs_py39

expected_calls = [
    [
        "Created hero:",
        {
            "id": 1,
            "name": "Deadpond",
            "age": None,
            "secret_name": "Dive Wilson",
            "team_id": 1,
        },
    ],
    [
        "Hero's team:",
        {"name": "Z-Force", "headquarters": "Sister Margaret's Bar", "id": 1},
    ],
]


@needs_py39
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.code_structure.tutorial002_py39 import app, database

    database.sqlite_url = "sqlite://"
    database.engine = create_engine(database.sqlite_url)
    app.engine = database.engine
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        app.main()
    assert calls == expected_calls
