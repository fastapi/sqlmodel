import asyncio
from typing import Any, Dict, List, Union
from unittest.mock import patch

from sqlmodel import AsyncSession, create_async_engine, select

from tests.conftest import get_testing_print_function


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


async def tutorial_async001():
    from docs_src.advanced.asyncio import tutorial001 as mod

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)
    with patch("builtins.print", new=new_print):
        await mod.main()
    async with AsyncSession(mod.engine) as session:
        heroes = (await session.exec(select(mod.Hero))).all()
    heroes_by_name = {hero.name: hero for hero in heroes}
    deadpond = heroes_by_name["Deadpond"]
    spider_boy = heroes_by_name["Spider-Boy"]
    rusty_man = heroes_by_name["Rusty-Man"]
    assert deadpond.name == "Deadpond"
    assert deadpond.age is None
    assert deadpond.id is not None
    assert deadpond.secret_name == "Dive Wilson"
    assert spider_boy.name == "Spider-Boy"
    assert spider_boy.age is None
    assert spider_boy.id is not None
    assert spider_boy.secret_name == "Pedro Parqueador"
    assert rusty_man.name == "Rusty-Man"
    assert rusty_man.age == 48
    assert rusty_man.id is not None
    assert rusty_man.secret_name == "Tommy Sharp"
    check_calls(calls)


def test_tutorial_001(clear_sqlmodel):
    asyncio.run(tutorial_async001())
