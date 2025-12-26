import importlib
import subprocess
from pathlib import Path
from types import ModuleType

import pytest

from ....conftest import needs_py310


@pytest.fixture(
    name="module",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(
        f"docs_src.tutorial.fastapi.app_testing.{request.param}.test_main"
    )
    return module


def test_run_tests(module: ModuleType):
    test_path = Path(module.__file__).resolve().parent
    top_level_path = Path(__file__).resolve().parent.parent.parent.parent.parent
    result = subprocess.run(
        [
            "coverage",
            "run",
            "--parallel-mode",
            "-m",
            "pytest",
            test_path,
        ],
        cwd=top_level_path,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout.decode("utf-8")
