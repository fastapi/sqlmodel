import pkg_resources
import pytest
import typer
from typer.testing import CliRunner

app = typer.Typer(name="dummy", help="Dummy app")


@pytest.fixture
def runner() -> CliRunner:
    yield CliRunner()


@pytest.fixture
def fake_cli() -> typer.Typer:
    entry_point = pkg_resources.EntryPoint(
        name="dummy", module_name="tests.test_cli.conftest", attrs=["app"]
    )
    entry_point.extras = []
    distribution = pkg_resources.Distribution()
    entry_point.dist = distribution
    distribution._ep_map = {"sqlmodel": {"dummy": entry_point}}
    pkg_resources.working_set.add(distribution, "dummy")

    return app
