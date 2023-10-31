from typer.testing import CliRunner


def test_import_module():
    from sqlmodel.cli import cli

    assert cli is not None
    assert cli.__name__ == "ok"