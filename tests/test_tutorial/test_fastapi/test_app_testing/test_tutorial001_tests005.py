import importlib

import pytest
from sqlmodel import Session

from docs_src.tutorial.fastapi.app_testing.tutorial001_py39 import main as app_mod
from docs_src.tutorial.fastapi.app_testing.tutorial001_py39 import (
    test_main_005 as test_mod,
)
from docs_src.tutorial.fastapi.app_testing.tutorial001_py39.test_main_005 import (
    session_fixture,
)

assert session_fixture, "This keeps the session fixture used below"


@pytest.fixture(name="prepare")
def prepare_fixture(clear_sqlmodel):
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel, but before the session_fixture
    # That's why the extra custom fixture here
    importlib.reload(app_mod)


def test_tutorial(prepare, session: Session):
    test_mod.test_create_hero(session)
