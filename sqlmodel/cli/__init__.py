"""
An extendable and simple CLI.
Load plugins from "sqlmodel" entry points.

The CLI depends on optional packages (Typer, Alembic). They are installed with
the ``migrations`` extra::

    pip install "sqlmodel[migrations]"
"""
from importlib.metadata import entry_points

_MISSING_DEPS_MESSAGE = (
    "The SQLModel CLI requires extra dependencies that are not installed.\n"
    'Install them with:\n\n    pip install "sqlmodel[migrations]"\n'
)

try:
    from typer import Typer
except ImportError as exc:  # pragma: no cover
    raise ImportError(_MISSING_DEPS_MESSAGE) from exc


cli = Typer()


def get_entry_points(plugin_name: str = "sqlmodel", app: Typer = cli) -> None:
    for entry_point in sorted(
        entry_points(group=plugin_name), key=lambda item: item.name
    ):
        try:
            plugin = entry_point.load()
        except ImportError as exc:  # pragma: no cover
            raise ImportError(_MISSING_DEPS_MESSAGE) from exc
        app.add_typer(plugin, name=plugin.info.name)


get_entry_points()
