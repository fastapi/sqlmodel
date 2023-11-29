import subprocess
from pathlib import Path

from ....conftest import needs_py39


@needs_py39
def test_run_tests(clear_sqlmodel):
    from docs_src.tutorial.fastapi.app_testing.tutorial001_py39 import test_main as mod

    test_path = Path(mod.__file__).resolve().parent
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
