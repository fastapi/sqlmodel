from typing import Any, Dict, List, Union
from unittest.mock import patch

from sqlmodel import create_engine

from ...conftest import get_testing_print_function


def check_calls(calls: List[List[Union[str, Dict[str, Any]]]]):
    assert calls[0][0] == {
        "name": "Deadpond",
        "secret_name": "Dive Wilson",
        "age": None,
        "id": 1,
    }
    assert calls[1][0] == {
        "name": "Spider-Boy",
        "secret_name": "Pedro Parqueador",
        "age": None,
        "id": 2,
    }
    assert calls[2][0] == {
        "name": "Rusty-Man",
        "secret_name": "Tommy Sharp",
        "age": 48,
        "id": 3,
    }


def test_tutorial_001(clear_sqlmodel):
    from docs_src.tutorial.select import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    check_calls(calls)


def test_tutorial_002(clear_sqlmodel):
    from docs_src.tutorial.select import tutorial002 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    check_calls(calls)
