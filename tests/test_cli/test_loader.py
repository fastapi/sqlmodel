from sqlmodel.cli import cli


def test_import_module() -> None:
    assert len(cli.registered_groups) == 1
    assert cli.registered_groups[0].name == "migrations"


def test_import_module_with_fake_cli(fake_cli) -> None:
    from sqlmodel.cli import cli, get_entry_points

    cli.registered_groups = []
    get_entry_points()
    assert len(cli.registered_groups) == 2
    assert cli.registered_groups[0].name == "dummy"
