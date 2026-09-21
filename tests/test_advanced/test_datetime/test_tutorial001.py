import importlib
from datetime import datetime, timezone
from types import ModuleType

import pytest
from sqlmodel import SQLModel, create_engine

from ...conftest import PrintMock, needs_py311


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
        pytest.param("tutorial001_py311", marks=needs_py311),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(f"docs_src.advanced.datetime.{request.param}")
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    before = datetime.now(timezone.utc)
    mod.main()
    after = datetime.now(timezone.utc)

    created_at = print_mock.calls[0][1]["created_at"]
    assert created_at.tzinfo is timezone.utc
    assert before <= created_at <= after
    assert print_mock.calls == [
        ["Event:", {"id": None, "created_at": created_at}],
        ["Event from database:", {"id": 1, "created_at": created_at}],
    ]
    assert print_mock.calls[1][1]["created_at"].tzinfo is timezone.utc

    table = SQLModel.metadata.tables["event"]
    assert table.c.created_at.type.timezone is True
