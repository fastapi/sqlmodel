import configparser
import logging
from pathlib import Path
from typing import List, Optional

import typer
from alembic import command
from alembic.config import Config
from typer import Typer
from typing_extensions import Annotated

logger = logging.getLogger(__name__)
migrations = Typer(
    name="migrations", help="Commands to interact with Alembic migrations"
)


@migrations.command()
def init(
    module: Path = Path("."),
    config_file: Path = Path("alembic.ini"),
    directory: Path = Path("migrations"),
    template: str = "generic",  # Should be Literal["generic", "multidb", "async"]
    target_metadata: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Initialize Alembic"""
    _config_file = module / config_file
    _directory = module / directory

    config = Config(_config_file)

    template_path = Path(__file__).parent.absolute() / "templates" / template

    command.init(
        config,
        str(_directory),
        template=str(template_path),
        package=True,
    )
    logger.debug("Inited alembic")
    if target_metadata:
        # Add target_metadata to alembic.ini

        updated_config = configparser.ConfigParser()
        updated_config.read(_config_file)
        updated_config["alembic"].update({"target_metadata": target_metadata})
        with open(_config_file, "w") as configfile:
            updated_config.write(configfile)
        logger.debug("Alembic defaults overrwritten")


@migrations.command()
def revision(
    module: Path = Path("."),
    config_file: Path = Path("alembic.ini"),
    message: Annotated[Optional[str], typer.Argument()] = None,
    autogenerate: bool = True,
    sql: bool = False,
    head: str = "head",
    splice: bool = False,
    # branch_label: Annotated[Optional[_RevIdType], typer.Argument()] = None,
    version_path: Annotated[Optional[str], typer.Argument()] = None,
    rev_id: Annotated[Optional[str], typer.Argument()] = None,
    depends_on: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Create a new Alembic revision"""
    config = Config(module / config_file)
    command.revision(
        config,
        message=message,
        autogenerate=autogenerate,
        sql=sql,
        head=head,
        splice=splice,
        # branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
        depends_on=depends_on,
    )


@migrations.command()
def show(
    module: Path = Path("."), config_file: Path = Path("alembic.ini"), rev: str = "head"
) -> None:
    """Show the revision"""
    config = Config(module / config_file)
    # Untyped function in Alembic
    command.show(config, rev)  # type: ignore


def merge(
    revisions: List[str],
    module: Path = Path("."),
    config_file: Path = Path("alembic.ini"),
    message: Annotated[Optional[str], typer.Argument()] = None,
    branch_label: Annotated[Optional[List[str]], typer.Argument()] = None,
    rev_id: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Merge two revisions together, creating a new migration file"""
    config = Config(module / config_file)
    command.merge(
        config,
        revisions,
        message=message,
        branch_label=branch_label,
        rev_id=rev_id,
    )


@migrations.command()
def upgrade(
    revision: str = "head",
    module: Path = Path("."),
    config_file: Path = Path("alembic.ini"),
    sql: bool = False,
    tag: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Upgrade to the given revision"""
    config = Config(module / config_file)
    command.upgrade(config, revision)


@migrations.command()
def downgrade(
    revision: str = "head",
    module: Path = Path("."),
    config_file: Path = Path("alembic.ini"),
    sql: bool = False,
    tag: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Downgrade to the given revision"""
    config = Config(module / config_file)
    command.downgrade(config, revision)
