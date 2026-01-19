import importlib
from types import ModuleType

import pytest
from sqlmodel import create_engine

from ...conftest import PrintMock, needs_py310

expected_calls = [
    [
        "Hero:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": None,
        },
    ],
    [
        "Updated hero:",
        {
            "id": 2,
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": 16,
        },
    ],
]


@pytest.fixture(name="module")
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    module = importlib.import_module(f"docs_src.tutorial.update.{request.param}")
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(module.sqlite_url)
    return module


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial001(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls


@pytest.mark.parametrize(
    "module",
    [
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
    indirect=True,
)
def test_tutorial002(print_mock: PrintMock, module: ModuleType):
    module.main()
    assert print_mock.calls == expected_calls
