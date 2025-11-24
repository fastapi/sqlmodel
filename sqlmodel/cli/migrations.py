import os
import re
from pathlib import Path
from typing import Optional

import typer
from alembic.autogenerate import produce_migrations, render_python_code
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, pool

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

migrations_app = typer.Typer()


def get_config_from_pyproject() -> dict:
    """Load and return the [tool.sqlmodel] configuration from pyproject.toml."""
    pyproject_path = Path.cwd() / "pyproject.toml"

    if not pyproject_path.exists():
        raise ValueError(
            "Could not find pyproject.toml in the current directory. "
            "Please create one with [tool.sqlmodel] section containing 'models = \"your.models.path\"'"
        )

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    # Try to get [tool.sqlmodel] section
    if "tool" not in config or "sqlmodel" not in config["tool"]:
        raise ValueError(
            "No [tool.sqlmodel] section found in pyproject.toml. "
            "Please add:\n\n"
            "[tool.sqlmodel]\n"
            "models = \"your.models.path\"\n"
        )

    return config["tool"]["sqlmodel"]


def get_models_path_from_config() -> str:
    """Get the models path from pyproject.toml configuration."""
    sqlmodel_config = get_config_from_pyproject()

    if "models" not in sqlmodel_config:
        raise ValueError(
            "No 'models' key found in [tool.sqlmodel] section. "
            "Please add:\n\n"
            "[tool.sqlmodel]\n"
            "models = \"your.models.path\"\n"
        )

    return sqlmodel_config["models"]


def get_migrations_dir(migrations_path: Optional[str] = None) -> Path:
    """Get the migrations directory path.

    Priority:
    1. Explicit migrations_path parameter
    2. migrations_path in [tool.sqlmodel] in pyproject.toml
    3. Default to ./migrations
    """
    if migrations_path:
        return Path(migrations_path)

    # Try to get from config
    try:
        sqlmodel_config = get_config_from_pyproject()
        if "migrations_path" in sqlmodel_config:
            return Path(sqlmodel_config["migrations_path"])
    except ValueError:
        # No pyproject.toml or no [tool.sqlmodel] section, use default
        pass

    return Path.cwd() / "migrations"


def get_alembic_config(migrations_dir: Path) -> Config:
    """Create an Alembic config object programmatically without ini file."""
    config = Config()
    config.set_main_option("script_location", str(migrations_dir))
    config.set_main_option("sqlalchemy.url", "")  # Will be set by env.py
    return config


def get_next_migration_number(migrations_dir: Path) -> str:
    """Get the next sequential migration number."""
    if not migrations_dir.exists():
        return "0001"

    migration_files = list(migrations_dir.glob("*.py"))
    if not migration_files:
        return "0001"

    numbers = []
    for f in migration_files:
        match = re.match(r"^(\d{4})_", f.name)
        if match:
            numbers.append(int(match.group(1)))

    if not numbers:
        return "0001"

    return f"{max(numbers) + 1:04d}"


def get_metadata(models_path: str):
    """Import and return SQLModel metadata."""
    import sys
    from importlib import import_module

    # Add current directory to Python path
    sys.path.insert(0, str(Path.cwd()))

    try:
        # Import the module containing the models
        models_module = import_module(models_path)

        # Get SQLModel from the module or import it
        if hasattr(models_module, "SQLModel"):
            return models_module.SQLModel.metadata
        else:
            # Try importing SQLModel from sqlmodel
            from sqlmodel import SQLModel

            return SQLModel.metadata
    except ImportError as e:
        raise ValueError(
            f"Failed to import models from '{models_path}': {e}\n"
            f"Make sure the module exists and is importable from the current directory."
        )


def get_current_revision(db_url: str) -> Optional[str]:
    """Get the current revision from the database."""
    import sqlalchemy as sa

    engine = create_engine(db_url, poolclass=pool.NullPool)

    # Create alembic_version table if it doesn't exist
    with engine.begin() as connection:
        connection.execute(
            sa.text("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """)
        )

    # Get current revision
    with engine.connect() as connection:
        result = connection.execute(sa.text("SELECT version_num FROM alembic_version"))
        row = result.first()
        return row[0] if row else None


def generate_migration_ops(db_url: str, metadata):
    """Generate migration operations by comparing metadata to database."""

    engine = create_engine(db_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        migration_context = MigrationContext.configure(connection)
        # Use produce_migrations which returns actual operation objects
        migration_script = produce_migrations(migration_context, metadata)

    return migration_script.upgrade_ops, migration_script.downgrade_ops


@migrations_app.command()
def create(
    message: str = typer.Option(..., "--message", "-m", help="Migration message"),
    migrations_path: Optional[str] = typer.Option(
        None, "--path", "-p", help="Path to migrations directory"
    ),
) -> None:
    """Create a new migration with autogenerate."""
    migrations_dir = get_migrations_dir(migrations_path)

    # Get models path from pyproject.toml
    try:
        models = get_models_path_from_config()
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    # Create migrations directory if it doesn't exist
    migrations_dir.mkdir(parents=True, exist_ok=True)

    # Get next migration number
    migration_number = get_next_migration_number(migrations_dir)

    # Create slug from message
    # TODO: truncate, handle special characters
    slug = message.lower().replace(" ", "_")
    slug = re.sub(r"[^a-z0-9_]", "", slug)

    filename = f"{migration_number}_{slug}.py"
    filepath = migrations_dir / filename

    typer.echo(f"Creating migration: {filename}")

    try:
        # Get database URL
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError(
                "DATABASE_URL environment variable is not set. "
                "Please set it to your database connection string."
            )

        # Get metadata
        metadata = get_metadata(models)

        # Check if there are pending migrations that need to be applied
        current_revision = get_current_revision(db_url)
        existing_migrations = sorted(
            [f for f in migrations_dir.glob("*.py") if f.name != "__init__.py"]
        )

        if existing_migrations:
            # Get the latest migration file
            latest_migration_file = existing_migrations[-1]
            content = latest_migration_file.read_text()
            # Extract revision = "..." from the file
            match = re.search(
                r'^revision = ["\']([^"\']+)["\']', content, re.MULTILINE
            )
            if match:
                latest_file_revision = match.group(1)
                # Check if database is up to date
                if current_revision != latest_file_revision:
                    typer.echo(
                        f"Error: Database is not up to date. Current revision: {current_revision or 'None'}, "
                        f"Latest migration: {latest_file_revision}",
                        err=True,
                    )
                    typer.echo(
                        "Please run 'sqlmodel migrations migrate' to apply pending migrations before creating a new one.",
                        err=True,
                    )
                    raise typer.Exit(1)

        # Generate migration operations
        upgrade_ops_obj, downgrade_ops_obj = generate_migration_ops(db_url, metadata)

        # Render upgrade
        if upgrade_ops_obj:
            upgrade_code = render_python_code(upgrade_ops_obj).strip()
        else:
            upgrade_code = "pass"

        # Render downgrade
        if downgrade_ops_obj:
            downgrade_code = render_python_code(downgrade_ops_obj).strip()
        else:
            # TODO: space :)
            downgrade_code = "pass"

        # Remove Alembic comments to check if migrations are actually empty
        def extract_code_without_comments(code: str) -> str:
            """Extract actual code, removing Alembic auto-generated comments."""
            lines = code.split("\n")
            actual_lines = []
            for line in lines:
                # Skip Alembic comment lines
                if not line.strip().startswith("# ###"):
                    actual_lines.append(line)
            return "\n".join(actual_lines).strip()

        upgrade_code_clean = extract_code_without_comments(upgrade_code)
        downgrade_code_clean = extract_code_without_comments(downgrade_code)

        # Only reject empty migrations if there are already existing migrations
        # (i.e., this is not the first migration)
        if (
            upgrade_code_clean == "pass"
            and downgrade_code_clean == "pass"
            and len(existing_migrations) > 0
        ):
            # TODO: better message
            typer.echo(
                "Empty migrations are not allowed"
            )  # TODO: unless you pass `--empty`
            raise typer.Exit(1)

        # Generate revision ID from filename (without .py extension)
        revision_id = f"{migration_number}_{slug}"

        # Get previous revision by reading the last migration file's revision ID
        down_revision = None
        if existing_migrations:
            # Read the last migration file to get its revision ID
            last_migration = existing_migrations[-1]
            content = last_migration.read_text()
            # Extract revision = "..." from the file
            import re as regex_module

            match = regex_module.search(
                r'^revision = ["\']([^"\']+)["\']', content, regex_module.MULTILINE
            )
            if match:
                down_revision = match.group(1)

        # Check if we need to import sqlmodel
        needs_sqlmodel = "sqlmodel" in upgrade_code or "sqlmodel" in downgrade_code

        # Generate migration file - build without f-strings to avoid % issues
        lines: list[str] = []
        lines.append(f'"""{message}"""')
        lines.append("")
        lines.append("import sqlalchemy as sa")
        if needs_sqlmodel:
            lines.append("import sqlmodel")
        lines.append("from alembic import op")
        lines.append("")
        lines.append('revision = "' + revision_id + '"')
        lines.append("down_revision = " + repr(down_revision))
        lines.append("depends_on = None")
        lines.append("")
        lines.append("")
        lines.append("def upgrade() -> None:")

        # Add upgrade code with proper indentation
        for line in upgrade_code.split("\n"):
            lines.append(line)

        lines.append("")
        lines.append("")
        lines.append("def downgrade() -> None:")

        # Add downgrade code with proper indentation
        for line in downgrade_code.split("\n"):
            lines.append(line)

        migration_content = "\n".join(lines)

        filepath.write_text(migration_content)

        typer.echo(f"✓ Created migration: {filename}")

    except ValueError as e:
        typer.echo(f"Error creating migration: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        import traceback

        typer.echo(f"Error creating migration: {e}", err=True)
        typer.echo("\nFull traceback:", err=True)
        traceback.print_exc()
        raise typer.Exit(1)


def get_pending_migrations(
    migrations_dir: Path, current_revision: Optional[str]
) -> list[Path]:
    """Get list of pending migration files."""
    all_migrations = sorted(
        [
            f
            for f in migrations_dir.glob("*.py")
            if f.name != "__init__.py" and f.name != "env.py"
        ]
    )

    if not current_revision:
        return all_migrations

    # Find migrations after the current revision
    pending = []
    found_current = False
    for migration_file in all_migrations:
        if found_current:
            pending.append(migration_file)
        elif migration_file.stem == current_revision:
            found_current = True

    return pending


def apply_migrations_programmatically(
    migrations_dir: Path, db_url: str, models: str
) -> None:
    """Apply migrations programmatically without env.py."""
    import importlib.util

    import sqlalchemy as sa

    # Get metadata
    metadata = get_metadata(models)

    # Create engine
    engine = create_engine(db_url, poolclass=pool.NullPool)

    # Create alembic_version table if it doesn't exist (outside transaction)
    with engine.begin() as connection:
        connection.execute(
            sa.text("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL,
                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
        """)
        )

    # Get current revision
    with engine.connect() as connection:
        result = connection.execute(sa.text("SELECT version_num FROM alembic_version"))
        row = result.first()
        current_revision = row[0] if row else None

    # Get pending migrations
    pending_migrations = get_pending_migrations(migrations_dir, current_revision)

    if not pending_migrations:
        typer.echo("  No pending migrations")
        return

    # Run each migration
    for migration_file in pending_migrations:
        revision_id = migration_file.stem
        typer.echo(f"  Applying: {revision_id}")

        # Execute each migration in its own transaction
        with engine.begin() as connection:
            # Create migration context
            migration_context = MigrationContext.configure(
                connection, opts={"target_metadata": metadata}
            )

            # Load the migration module
            spec = importlib.util.spec_from_file_location(revision_id, migration_file)
            if not spec or not spec.loader:
                raise ValueError(f"Could not load migration: {migration_file}")

            module = importlib.util.module_from_spec(spec)

            # Also make sqlalchemy and sqlmodel available
            import sqlmodel

            module.sa = sa  # type: ignore
            module.sqlmodel = sqlmodel  # type: ignore

            # Execute the module to define the functions
            spec.loader.exec_module(module)

            # Create operations context and run upgrade within ops.invoke_for_target
            from alembic.operations import ops

            with ops.Operations.context(migration_context):
                # Now op proxy is available via alembic.op
                from alembic import op as alembic_op

                module.op = alembic_op  # type: ignore

                # Execute upgrade
                module.upgrade()

            # Update alembic_version table
            if current_revision:
                connection.execute(
                    sa.text("UPDATE alembic_version SET version_num = :version"),
                    {"version": revision_id},
                )
            else:
                connection.execute(
                    sa.text(
                        "INSERT INTO alembic_version (version_num) VALUES (:version)"
                    ),
                    {"version": revision_id},
                )

            current_revision = revision_id


@migrations_app.command()
def migrate(
    migrations_path: Optional[str] = typer.Option(
        None, "--path", "-p", help="Path to migrations directory"
    ),
) -> None:
    """Apply all pending migrations to the database."""
    migrations_dir = get_migrations_dir(migrations_path)

    # Get models path from pyproject.toml
    try:
        models = get_models_path_from_config()
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if not migrations_dir.exists():
        typer.echo(
            f"Error: {migrations_dir} not found. Run 'sqlmodel migrations init' first.",
            err=True,
        )
        raise typer.Exit(1)

    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        typer.echo("Error: DATABASE_URL environment variable is not set.", err=True)
        raise typer.Exit(1)

    typer.echo("Applying migrations...")

    try:
        apply_migrations_programmatically(migrations_dir, db_url, models)
        typer.echo("✓ Migrations applied successfully")
    except Exception as e:
        typer.echo(f"Error applying migrations: {e}", err=True)
        raise typer.Exit(1)
