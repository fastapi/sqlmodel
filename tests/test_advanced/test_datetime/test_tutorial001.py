import importlib
from datetime import UTC, datetime, timedelta
from types import ModuleType

import pytest
from sqlalchemy import Engine
from sqlmodel import SQLModel

from ...conftest import PrintMock


@pytest.fixture(name="mod")
def get_module(database_engine: Engine) -> ModuleType:
    mod = importlib.import_module("docs_src.advanced.datetime.tutorial001")
    mod.engine = database_engine
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    before = datetime.now(UTC)
    mod.main()
    after = datetime.now(UTC)

    created_at = print_mock.calls[0][1]["created_at"]
    assert created_at.tzinfo is UTC
    assert before <= created_at <= after
    stored_created_at = print_mock.calls[1][1]["created_at"]
    assert stored_created_at.tzinfo is UTC
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
