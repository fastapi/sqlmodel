import sys
from typing import Any, Dict, List, Union
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from tests.conftest import get_testing_print_function


def check_calls(calls: List[List[Union[str, Dict[str, Any]]]]) -> None:
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


beforePYTHON3_9 = sys.version_info < (3, 9)
reasonPEP593 = "Annotations(PEP593 https://peps.python.org/pep-0593/) only compatible with Python ver >= 3.9"


@pytest.mark.skipif(beforePYTHON3_9, reason=reasonPEP593)
@pytest.mark.asyncio
async def test_tutorial_async_001(clear_sqlmodel: Any) -> None:
    from docs_src.tutorial_async.select_async import tutorial001_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls: List[Any] = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)


@pytest.mark.skipif(beforePYTHON3_9, reason=reasonPEP593)
@pytest.mark.asyncio
async def test_tutorial_async_002(clear_sqlmodel: Any) -> None:
    from docs_src.tutorial_async.select_async import tutorial002_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls: List[Any] = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)
