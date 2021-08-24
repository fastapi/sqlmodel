from typing import Any, Dict, List, Union
from unittest.mock import patch

from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

from ....conftest import get_testing_print_function

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


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.define_relationship_attributes import (
        tutorial001 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == expected_calls
