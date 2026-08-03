from importlib.metadata import EntryPoint

import pytest
import typer
from typer.testing import CliRunner

app = typer.Typer(name="dummy", help="Dummy app")


@pytest.fixture
def runner() -> CliRunner:
    yield CliRunner()


@pytest.fixture
def fake_cli(monkeypatch: pytest.MonkeyPatch) -> typer.Typer:
    import sqlmodel.cli

    existing_entry_points = sqlmodel.cli.entry_points(group="sqlmodel")
    entry_point = EntryPoint(
        name="dummy", value="tests.test_cli.conftest:app", group="sqlmodel"
    )
    monkeypatch.setattr(
        sqlmodel.cli,
        "entry_points",
        lambda *, group: [*existing_entry_points, entry_point],
    )
    return app
