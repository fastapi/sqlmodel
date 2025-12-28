import shutil
import subprocess
import sys
from collections.abc import Generator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Union
from unittest.mock import patch

import pytest
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.main import default_registry

top_level_path = Path(__file__).resolve().parent.parent
docs_src_path = top_level_path / "docs_src"


@pytest.fixture(autouse=True)
def clear_sqlmodel() -> Any:
    # Clear the tables in the metadata for the default base model
    SQLModel.metadata.clear()
    # Clear the Models associated with the registry, to avoid warnings
    default_registry.dispose()
    yield
    SQLModel.metadata.clear()
    default_registry.dispose()


@pytest.fixture()
def cov_tmp_path(tmp_path: Path) -> Generator[Path, None, None]:
    yield tmp_path
    for coverage_path in tmp_path.glob(".coverage*"):
        coverage_destiny_path = top_level_path / "coverage" / coverage_path.name
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
    calls: list[list[Union[str, dict[str, Any]]]],
) -> Callable[..., Any]:
    def new_print(*args: Any) -> None:
        data: list[Any] = []
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


@dataclass
class PrintMock:
    calls: list[Any] = field(default_factory=list)


@pytest.fixture(name="print_mock")
def print_mock_fixture() -> Generator[PrintMock, None, None]:
    print_mock = PrintMock()
    new_print = get_testing_print_function(print_mock.calls)
    with patch("builtins.print", new=new_print):
        yield print_mock


needs_py310 = pytest.mark.skipif(
    sys.version_info < (3, 10), reason="requires python3.10+"
)
