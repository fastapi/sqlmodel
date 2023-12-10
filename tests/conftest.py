import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import pytest
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel._compat import IS_PYDANTIC_V2
from sqlmodel.main import default_registry

top_level_path = Path(__file__).resolve().parent.parent
docs_src_path = top_level_path / "docs_src"


@pytest.fixture()
def clear_sqlmodel():
    # Clear the tables in the metadata for the default base model
    SQLModel.metadata.clear()
    # Clear the Models associated with the registry, to avoid warnings
    default_registry.dispose()
    yield
    SQLModel.metadata.clear()
    default_registry.dispose()


@pytest.fixture()
def cov_tmp_path(tmp_path: Path):
    yield tmp_path
    for coverage_path in tmp_path.glob(".coverage*"):
        coverage_destiny_path = top_level_path / coverage_path.name
        shutil.copy(coverage_path, coverage_destiny_path)


def coverage_run(*, module: str, cwd: Union[str, Path]) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [
            "coverage",
            "run",
            "--parallel-mode",
            "--source=docs_src,tests,sqlmodel",
            "-m",
            module,
        ],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
    )
    return result


def get_testing_print_function(
    calls: List[List[Union[str, Dict[str, Any]]]],
) -> Callable[..., Any]:
    def new_print(*args):
        data = []
        for arg in args:
            if isinstance(arg, BaseModel):
                data.append(arg.model_dump())
            elif isinstance(arg, list):
                new_list = []
                for item in arg:
                    if isinstance(item, BaseModel):
                        new_list.append(item.model_dump())
                data.append(new_list)
            else:
                data.append(arg)
        calls.append(data)

    return new_print


needs_pydanticv2 = pytest.mark.skipif(not IS_PYDANTIC_V2, reason="requires Pydantic v2")
needs_pydanticv1 = pytest.mark.skipif(IS_PYDANTIC_V2, reason="requires Pydantic v1")

needs_py39 = pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9+")
needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
