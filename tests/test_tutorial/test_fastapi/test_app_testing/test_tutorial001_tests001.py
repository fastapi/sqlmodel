import importlib
from typing import Any, Dict, List, Union
from unittest.mock import patch

from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool

from docs_src.tutorial.fastapi.app_testing.tutorial001 import test_main_001 as test_mod
from docs_src.tutorial.fastapi.app_testing.tutorial001 import main as app_mod

import pytest

@pytest.fixture(name="prepare", autouse=True)
def prepare_fixture(clear_sqlmodel):
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel
    importlib.reload(app_mod)
    importlib.reload(test_mod)

def test_tutorial():
    test_mod.test_create_hero()
