import pytest
from typing import Any, Dict, List, Union
from unittest.mock import patch

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import MetaData, Session, SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine

from tests.conftest import get_testing_print_function


def check_calls(calls: List[List[Union[str, Dict[str, Any]]]]):
    assert calls[0][0] == [
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


@pytest.mark.asyncio
async def test_tutorial_003(clear_sqlmodel):
    from docs_src.tutorial_async.select_async import tutorial003_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)

    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)


@pytest.mark.asyncio
async def test_tutorial_004(clear_sqlmodel):
    from docs_src.tutorial_async.select_async import tutorial004_async as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    check_calls(calls)
