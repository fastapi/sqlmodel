import pytest


@pytest.fixture(name="prepare", autouse=True)
def prepare_fixture(clear_sqlmodel):
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel
    pass


def test_tutorial():
    from docs_src.tutorial.fastapi.app_testing.tutorial001 import (
        test_main_001 as test_mod,
    )

    test_mod.test_create_hero()
