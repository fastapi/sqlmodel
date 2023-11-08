"""
An extendable and simple CLI.
Load plugins from "sqlmodel" entry points.
"""
import pkg_resources
from typer import Typer

cli = Typer()


def get_entry_points(plugin_name: str = "sqlmodel", app: Typer = cli) -> None:
    for entry_point in pkg_resources.iter_entry_points(plugin_name):
        plugin = entry_point.load()
        cli.add_typer(plugin, name=plugin.info.name)


get_entry_points()
