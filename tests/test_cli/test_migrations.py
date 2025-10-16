import shutil
from pathlib import Path

import pytest
from inline_snapshot import external, register_format_alias
from sqlmodel.cli import app
from typer.testing import CliRunner

register_format_alias(".py", ".txt")

runner = CliRunner()


HERE = Path(__file__).parent

register_format_alias(".html", ".txt")


def test_create_first_migration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Test creating the first migration with an empty database."""
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
            str(migrations_dir),
        ],
    )

    assert result.exit_code == 0, f"Command failed: {result.stdout}"
    assert "✓ Created migration:" in result.stdout

    migration_files = sorted(
        [str(f.relative_to(tmp_path)) for f in migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]

    migration_file = migrations_dir / "0001_initial_migration.py"

    assert migration_file.read_text() == external(
        "uuid:f1182584-912e-4f31-9d79-2233e5a8a986.py"
    )


# TODO: to force migration you need to pass `--empty`s
def test_running_migration_twice_only_generates_migration_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
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
            str(migrations_dir),
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
            str(migrations_dir),
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
            str(migrations_dir),
        ],
    )

    assert result.exit_code == 1
    assert "Empty migrations are not allowed" in result.stdout

    migration_files = sorted(
        [str(f.relative_to(tmp_path)) for f in migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]


def test_cannot_create_migration_with_pending_migrations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Test that creating a migration fails if there are unapplied migrations."""
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
            str(migrations_dir),
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
            str(migrations_dir),
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
        [str(f.relative_to(tmp_path)) for f in migrations_dir.glob("*.py")]
    )

    assert migration_files == [
        "migrations/0001_initial_migration.py",
    ]
