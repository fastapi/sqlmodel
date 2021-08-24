import importlib

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from docs_src.tutorial.fastapi.app_testing.tutorial001 import main as app_mod
from docs_src.tutorial.fastapi.app_testing.tutorial001 import test_main_006 as test_mod
from docs_src.tutorial.fastapi.app_testing.tutorial001.test_main_006 import (
    client_fixture,
    session_fixture,
)

assert session_fixture, "This keeps the session fixture used below"
assert client_fixture, "This keeps the client fixture used below"


@pytest.fixture(name="prepare")
def prepare_fixture(clear_sqlmodel):
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel, but before the session_fixture
    # That's why the extra custom fixture here
    importlib.reload(app_mod)


def test_tutorial(prepare, session: Session, client: TestClient):
    test_mod.test_create_hero(client)
