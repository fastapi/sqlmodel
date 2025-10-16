import typer

from .migrations import migrations_app

app = typer.Typer()
app.add_typer(migrations_app, name="migrations")


def main() -> None:
    app()
