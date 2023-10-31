import configparser
import logging
from pathlib import Path
from typing import Literal, Optional, Union

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
    module: Path = ".",
    config_file: Path = "alembic.ini",
    script_location: Path = "migrations",
    template: str = "generic",  # Should be Literal["generic", "multidb", "async"]
    target_metadata: Annotated[Optional[str], typer.Argument()] = None,
):
    """Initialize Alembic"""
    _config_file = module / config_file
    _script_location = module / script_location

    config = Config(_config_file)

    template_path = Path(__file__).parent.absolute() / "templates" / template

    command.init(
        config,
        _script_location,
        template=template_path,
        package=True,
    )
    logger.debug(f"Inited alembic")
    # Add target_metadata to alembic.ini

    updated_config = configparser.ConfigParser()
    updated_config.read(_config_file)
    updated_config["alembic"].update({"target_metadata": target_metadata})
    with open(_config_file, "w") as configfile:
        updated_config.write(configfile)
    logger.debug(f"Alembic defaults overrwritten")
