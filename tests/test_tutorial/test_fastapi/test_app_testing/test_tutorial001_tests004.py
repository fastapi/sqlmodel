import importlib

import pytest


@pytest.fixture(name="prepare", autouse=True)
def prepare_fixture(clear_sqlmodel):
    # Import after clear_sqlmodel to avoid table registration conflicts
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import main as app_mod
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import (
        test_main_004 as test_mod,
    )

    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel
    importlib.reload(app_mod)
    importlib.reload(test_mod)


def test_tutorial(prepare):
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import (
        test_main_004 as test_mod,
    )

    test_mod.test_create_hero()
