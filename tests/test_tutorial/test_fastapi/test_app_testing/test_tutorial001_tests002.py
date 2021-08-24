import importlib

import pytest

from docs_src.tutorial.fastapi.app_testing.tutorial001 import main as app_mod
from docs_src.tutorial.fastapi.app_testing.tutorial001 import test_main_002 as test_mod


@pytest.fixture(name="prepare", autouse=True)
def prepare_fixture(clear_sqlmodel):
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel
    importlib.reload(app_mod)
    importlib.reload(test_mod)


def test_tutorial():
    test_mod.test_create_hero()
