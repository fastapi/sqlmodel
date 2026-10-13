import importlib
from datetime import datetime, timedelta, timezone
from types import ModuleType

import pytest
from sqlalchemy import Engine
from sqlmodel import SQLModel

from ...conftest import PrintMock, needs_py311


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py310"),
        pytest.param("tutorial001_py311", marks=needs_py311),
    ],
)
def get_module(request: pytest.FixtureRequest, database_engine: Engine) -> ModuleType:
    mod = importlib.import_module(f"docs_src.advanced.datetime.{request.param}")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    before = datetime.now(timezone.utc)
    mod.main()
    after = datetime.now(timezone.utc)

    created_at = print_mock.calls[0][1]["created_at"]
    assert created_at.tzinfo is timezone.utc
    assert before <= created_at <= after
    stored_created_at = print_mock.calls[1][1]["created_at"]
    assert stored_created_at.tzinfo is timezone.utc
    if mod.engine.dialect.name in {"mysql", "mariadb"}:
        # The default DATETIME columns store whole seconds.
        assert abs(stored_created_at - created_at) < timedelta(seconds=1)
    else:
        assert stored_created_at == created_at
    assert print_mock.calls == [
        ["Event:", {"id": None, "created_at": created_at}],
        ["Event from database:", {"id": 1, "created_at": stored_created_at}],
    ]

    table = SQLModel.metadata.tables["event"]
    assert table.c.created_at.type.timezone is True
