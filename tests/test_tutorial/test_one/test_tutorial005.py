import importlib
from types import ModuleType

import pytest
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, create_engine, delete

from ...conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.tutorial.one.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    with pytest.raises(NoResultFound):
        mod.main()
    with Session(mod.engine) as session:
        # TODO: create delete() function
        # TODO: add overloads for .exec() with delete object
        session.exec(delete(mod.Hero))
        session.add(mod.Hero(name="Test Hero", secret_name="Secret Test Hero", age=24))
        session.commit()

    mod.select_heroes()
    assert print_mock.calls == [
        [
            "Hero:",
            {
                "id": 1,
                "name": "Test Hero",
                "secret_name": "Secret Test Hero",
                "age": 24,
            },
        ]
    ]
