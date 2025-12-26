import importlib
import sys
from dataclasses import dataclass
from types import ModuleType

import pytest

from tests.conftest import needs_py310


@dataclass
class Modules:
    app: ModuleType
    test: ModuleType


@pytest.fixture(
    name="modules_path",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_modules_path(request: pytest.FixtureRequest) -> str:
    return f"docs_src.tutorial.fastapi.app_testing.{request.param}"


@pytest.fixture(name="modules")
def load_modules(clear_sqlmodel, modules_path: str) -> Modules:
    # Trigger side effects of registering table models in SQLModel
    # This has to be called after clear_sqlmodel
    app_mod_path = f"{modules_path}.main"
    if app_mod_path in sys.modules:
        app_mod = sys.modules[app_mod_path]
        importlib.reload(app_mod)
    else:
        app_mod = importlib.import_module(app_mod_path)  # pragma: no cover
    test_mod = importlib.import_module(f"{modules_path}.test_main_002")
    return Modules(app=app_mod, test=test_mod)


def test_tutorial(modules: Modules):
    modules.test.test_create_hero()
