import importlib
from datetime import datetime, timezone
from types import ModuleType

import pytest
from sqlmodel import SQLModel

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    return importlib.import_module(f"docs_src.advanced.datetime.{request.param}")


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    mod.main()
    assert print_mock.calls == [
        ["Event:", {"id": None, "created_at": datetime(2026, 1, 1, 12)}]
    ]

    aware = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    assert mod.Event.model_validate({"created_at": aware}).created_at == aware

    table = SQLModel.metadata.tables["event"]
    assert table.c.created_at.type.timezone is False
