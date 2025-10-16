import shutil
from pathlib import Path
from typing import NamedTuple

import pytest
from inline_snapshot import external, register_format_alias
from sqlmodel.cli import app
from typer.testing import CliRunner

register_format_alias(".py", ".txt")

runner = CliRunner()


HERE = Path(__file__).parent

register_format_alias(".html", ".txt")


class MigrationTestEnv(NamedTuple):
    """Test environment for migrations."""
    tmp_path: Path
    db_path: Path
    db_url: str
    migrations_dir: Path
    models_dir: Path
    models_file: Path


@pytest.fixture
def migration_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> MigrationTestEnv:
    """Set up a test environment for migrations."""
    db_path = tmp_path / "test.db"
    db_url = f"sqlite:///{db_path}"
    migrations_dir = tmp_path / "migrations"

    model_source = HERE / "./fixtures/models_initial.py"

    models_dir = tmp_path / "test_models"
    models_dir.mkdir()

    (models_dir / "__init__.py").write_text("")
    models_file = models_dir / "models.py"

    shutil.copy(model_source, models_file)

    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.chdir(tmp_path)

    return MigrationTestEnv(
        tmp_path=tmp_path,
        db_path=db_path,
        db_url=db_url,
        migrations_dir=migrations_dir,
        models_dir=models_dir,
        models_file=models_file,
    )


def test_create_first_migration(migration_env: MigrationTestEnv):
    """Test creating the first migration with an empty database."""
    # Run the create command
    result = runner.invoke(
        app,
        [
            "migrations",
            "create",
            "-m",
            "Initial migration",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    assert result.exit_code == 0, f"Command failed: {result.stdout}"
    assert "✓ Created migration:" in result.stdout

    migration_files = sorted(
        [str(f.relative_to(migration_env.tmp_path)) for f in migration_env.migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]

    migration_file = migration_env.migrations_dir / "0001_initial_migration.py"

    assert migration_file.read_text() == external(
        "uuid:f1182584-912e-4f31-9d79-2233e5a8a986.py"
    )


# TODO: to force migration you need to pass `--empty`s
def test_running_migration_twice_only_generates_migration_once(
    migration_env: MigrationTestEnv,
):
    """Test that running migration creation twice without changes fails."""
    # Run the create command
    result = runner.invoke(
        app,
        [
            "migrations",
            "create",
            "-m",
            "Initial migration",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    assert result.exit_code == 0, f"Command failed: {result.stdout}"
    assert "✓ Created migration:" in result.stdout

    # Apply the first migration to the database
    result = runner.invoke(
        app,
        [
            "migrations",
            "migrate",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    assert result.exit_code == 0, f"Migration failed: {result.stdout}"

    # Run the create command again (should fail with empty migration)
    result = runner.invoke(
        app,
        [
            "migrations",
            "create",
            "-m",
            "Initial migration",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    assert result.exit_code == 1
    assert "Empty migrations are not allowed" in result.stdout

    migration_files = sorted(
        [str(f.relative_to(migration_env.tmp_path)) for f in migration_env.migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]


def test_cannot_create_migration_with_pending_migrations(
    migration_env: MigrationTestEnv,
):
    """Test that creating a migration fails if there are unapplied migrations."""
    # Run the create command to create first migration
    result = runner.invoke(
        app,
        [
            "migrations",
            "create",
            "-m",
            "Initial migration",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    assert result.exit_code == 0, f"Command failed: {result.stdout}"
    assert "✓ Created migration:" in result.stdout

    # Try to create another migration WITHOUT applying the first one
    result = runner.invoke(
        app,
        [
            "migrations",
            "create",
            "-m",
            "Second migration",
            "--models",
            "test_models.models",
            "--path",
            str(migration_env.migrations_dir),
        ],
    )

    # Should fail because database is not up to date
    assert result.exit_code == 1
    # Error messages are printed to stderr, which Typer's CliRunner combines into output
    assert (
        "Database is not up to date" in result.stdout
        or "Database is not up to date" in str(result.output)
    )
    assert (
        "Please run 'sqlmodel migrations migrate'" in result.stdout
        or "Please run 'sqlmodel migrations migrate'" in str(result.output)
    )

    # Verify only one migration file exists
    migration_files = sorted(
        [str(f.relative_to(migration_env.tmp_path)) for f in migration_env.migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]
