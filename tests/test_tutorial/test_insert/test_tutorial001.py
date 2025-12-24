import importlib
from types import ModuleType

import pytest
from sqlmodel import Session, create_engine, select

from ...conftest import needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.insert.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(mod: ModuleType):
    mod.main()
    with Session(mod.engine) as session:
        heroes = session.exec(select(mod.Hero)).all()
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
