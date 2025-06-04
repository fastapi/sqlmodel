import importlib

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


@pytest.fixture(name="prepare")
def prepare_fixture(clear_sqlmodel):
    # Import after clear_sqlmodel to avoid table registration conflicts
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import main as app_mod
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import (
        test_main_005 as test_mod,
    )

    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel, but before the session_fixture
    # That's why the extra custom fixture here
    importlib.reload(app_mod)
    importlib.reload(test_mod)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_tutorial(prepare, session: Session):
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import (
        test_main_005 as test_mod,
    )

    test_mod.test_create_hero(session)
