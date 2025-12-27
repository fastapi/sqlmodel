import os
import subprocess
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent


def test_select_gen() -> None:
    env = os.environ.copy()
    env["CHECK_JINJA"] = "1"
    result = subprocess.run(
        [sys.executable, Path("scripts") / "generate_select.py"],
        env=env,
        check=True,
        cwd=root_path,
        capture_output=True,
    )
    print(result.stdout)
