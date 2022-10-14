import pytest
from unittest.mock import patch

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

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
    [
        "Hero:",
        {
            "age": None,
            "id": 1,
            "secret_name": "Dive Wilson",
            "team_id": 2,
            "name": "Deadpond",
        },
        "Team:",
        {"id": 2, "name": "Z-Force", "headquarters": "Sister Margaret’s Bar"},
    ],
    [
        "Hero:",
        {
            "age": 48,
            "id": 2,
            "secret_name": "Tommy Sharp",
            "team_id": 1,
            "name": "Rusty-Man",
        },
        "Team:",
        {"id": 1, "name": "Preventers", "headquarters": "Sharp Tower"},
    ],
    [
        "Hero:",
        {
            "age": None,
            "id": 3,
            "secret_name": "Pedro Parqueador",
            "team_id": None,
            "name": "Spider-Boy",
        },
        "Team:",
        None,
    ],
]


@pytest.mark.asyncio()
async def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial_async.connect_async.select_async import (
        tutorial003_async as mod,
    )

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        await mod.main()
    assert calls == expected_calls
