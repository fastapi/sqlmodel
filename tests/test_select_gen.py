import subprocess
import sys
from pathlib import Path

from .conftest import needs_py39

root_path = Path(__file__).parent.parent


@needs_py39
def test_select_gen() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/generate_select.py"],
        env={"CHECK_JINJA": "1"},
        check=True,
        cwd=root_path,
        capture_output=True,
    )
    print(result.stdout)
