import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List, Union
import pytest
from sqlmodel import SQLModel
from sqlmodel.main import default_registry
from pydantic import BaseModel

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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return result


def get_testing_print_function(
    calls: List[List[Union[str, Dict[str, Any]]]]
) -> Callable[..., Any]:
    def new_print(*args):
        data = []
        for arg in args:
            if isinstance(arg, BaseModel):
                data.append(arg.dict())
            elif isinstance(arg, list):
                new_list = []
                for item in arg:
                    if isinstance(item, BaseModel):
                        new_list.append(item.dict())
                data.append(new_list)
            else:
                data.append(arg)
        calls.append(data)

    return new_print
