from typing import Any, Dict, List, Union
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from tests.conftest import get_testing_print_function


def check_calls(calls: List[List[List[Union[str, Dict[str, Any]]]]]) -> None:
    expected_result: List[Union[str, Dict[str, Any]]] = [
        {
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "age": None,
            "id": 1,
        },
        {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
            "id": 2,
        },
        {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
            "id": 3,
        },
    ]

    assert calls[0][0] == expected_result


@pytest.mark.asyncio
async def test_tutorial_003(clear_sqlmodel: Any) -> None:
    from docs_src.tutorial_async.select_async import tutorial003_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)

    calls: List[Any] = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)


@pytest.mark.asyncio
async def test_tutorial_004(clear_sqlmodel: Any) -> None:
    from docs_src.tutorial_async.select_async import tutorial004_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls: List[Any] = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)
