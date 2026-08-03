"""
An extendable and simple CLI.
Load plugins from "sqlmodel" entry points.
"""
from importlib.metadata import entry_points

from typer import Typer

cli = Typer()


def get_entry_points(plugin_name: str = "sqlmodel", app: Typer = cli) -> None:
    for entry_point in sorted(entry_points(group=plugin_name), key=lambda item: item.name):
        plugin = entry_point.load()
        app.add_typer(plugin, name=plugin.info.name)


get_entry_points()
