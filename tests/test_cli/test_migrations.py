import configparser
from pathlib import Path

from sqlmodel.cli import cli


def test_base_init(tmpdir, runner):
    runner.invoke(cli, ["migrations", "init", "--module", str(tmpdir)])
    assert (Path(tmpdir) / "alembic.ini").exists()


def test_base_init_with_metadata(tmpdir, runner):
    runner.invoke(cli, ["migrations", "init", "--module", str(tmpdir), "path.to.Model"])
    config = configparser.ConfigParser()
    config.read(Path(tmpdir) / "alembic.ini")

    assert config["alembic"]["target_metadata"] == "path.to.Model"


def test_base_init_with_metadata_and_configfile(tmpdir, runner):
    runner.invoke(
        cli,
        [
            "migrations",
            "init",
            "--module",
            str(tmpdir),
            "--config-file",
            "foo.ini",
            "path.to.Model",
        ],
    )
    config = configparser.ConfigParser()
    config.read(Path(tmpdir) / "foo.ini")

    assert config["alembic"]["target_metadata"] == "path.to.Model"


def test_base_init_with_async_template(tmpdir, runner):
    runner.invoke(
        cli,
        ["migrations", "init", "--module", str(tmpdir), "--template", "async"],
    )
    with open(Path(tmpdir) / "migrations" / "README") as f:
        assert (
            f.read() == "Generic single-database configuration with an async dbapi.\n"
        )
