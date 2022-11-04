import sys
from typing import Any, List
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from tests.conftest import get_testing_print_function

expected_calls = [
    [
        "Created hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 2,
            "name": "Deadpond",
        },
    ],
    [
        "Created hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 1,
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
]


beforePYTHON3_9 = sys.version_info < (3, 9)
reasonPEP593 = "Annotations(PEP593 https://peps.python.org/pep-0593/) only compatible with Python ver >= 3.9"


@pytest.mark.skipif(beforePYTHON3_9, reason=reasonPEP593)
@pytest.mark.asyncio()
async def test_async_tutorial001(clear_sqlmodel: Any) -> None:
    from docs_src.tutorial_async.connect_async.insert_async import (
        tutorial001_async as mod,
    )

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls: List[Any] = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    assert calls == expected_calls
