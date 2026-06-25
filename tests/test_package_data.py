from importlib import resources


def test_sqlmodel_skill_file_is_packaged() -> None:
    skill_file = (
        resources.files("sqlmodel") / ".agents" / "skills" / "sqlmodel" / "SKILL.md"
    )

    assert skill_file.is_file()
