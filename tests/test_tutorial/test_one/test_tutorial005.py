import importlib
from types import ModuleType

import pytest
from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, delete

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial005_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.one.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    with pytest.raises(NoResultFound):
        mod.main()
    with Session(mod.engine) as session:
        # TODO: create delete() function
        # TODO: add overloads for .exec() with delete object
        session.exec(delete(mod.Hero))
        hero = mod.Hero(name="Test Hero", secret_name="Secret Test Hero", age=24)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        hero_id = hero.id
        assert hero_id is not None

    mod.select_heroes()
    assert print_mock.calls == [
        [
            "Hero:",
            {
                "id": hero_id,
                "name": "Test Hero",
                "secret_name": "Secret Test Hero",
                "age": 24,
            },
        ]
    ]
