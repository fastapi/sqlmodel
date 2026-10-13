import importlib
from datetime import datetime, timezone
from types import ModuleType

import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel

from ...conftest import PrintMock


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial005_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    return importlib.import_module(f"docs_src.advanced.datetime.{request.param}")


def test_tutorial(print_mock: PrintMock, mod: ModuleType) -> None:
    mod.main()
    assert print_mock.calls == [
        ["Event:", {"id": None, "created_at": datetime(2026, 1, 1, 12)}]
    ]

    with pytest.raises(ValidationError) as exc_info:
        mod.Event.model_validate(
            {"created_at": datetime(2026, 1, 1, 12, tzinfo=timezone.utc)}
        )
    errors = exc_info.value.errors()
    assert [(error["loc"], error["type"]) for error in errors] == [
        (("created_at",), "timezone_naive"),
    ]

    table = SQLModel.metadata.tables["event"]
    assert table.c.created_at.type.timezone is False
