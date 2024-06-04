import os
import subprocess
import sys
from pathlib import Path

from .conftest import needs_py39

root_path = Path(__file__).parent.parent


@needs_py39
def test_select_gen() -> None:
    env = os.environ.copy()
    env["CHECK_JINJA"] = "1"
    result = subprocess.run(
        [sys.executable, "scripts/generate_select.py"],
        env=env,
        check=True,
        cwd=root_path,
        capture_output=True,
    )
    print(result.stdout)
