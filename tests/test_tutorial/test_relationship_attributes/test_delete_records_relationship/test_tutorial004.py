import importlib
from types import ModuleType

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, create_engine, select

from ....conftest import PrintMock, needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    mod = importlib.import_module(
        f"docs_src.tutorial.relationship_attributes.cascade_delete_relationships.{request.param}"
    )
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    return mod


def test_tutorial(print_mock: PrintMock, mod: ModuleType):
    mod.create_db_and_tables()
    mod.create_heroes()
    mod.select_deleted_heroes()
    with Session(mod.engine) as session:
        team = session.exec(select(mod.Team).where(mod.Team.name == "Wakaland")).one()
        team.heroes.clear()
        session.add(team)
        session.commit()
    mod.delete_team()
    assert print_mock.calls == [
        [
            "Created hero:",
            {
                "age": None,
                "id": 1,
                "name": "Deadpond",
                "secret_name": "Dive Wilson",
                "team_id": 1,
            },
        ],
        [
            "Created hero:",
            {
                "age": 48,
                "id": 2,
                "name": "Rusty-Man",
                "secret_name": "Tommy Sharp",
                "team_id": 2,
            },
        ],
        [
            "Created hero:",
            {
                "age": None,
                "id": 3,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": None,
            },
        ],
        [
            "Updated hero:",
            {
                "age": None,
                "id": 3,
                "name": "Spider-Boy",
                "secret_name": "Pedro Parqueador",
                "team_id": 2,
            },
        ],
        [
            "Team Wakaland:",
            {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
        ],
        [
            "Black Lion has no team:",
            {
                "age": 35,
                "id": 4,
                "name": "Black Lion",
                "secret_name": "Trevor Challa",
                "team_id": 3,
            },
        ],
        [
            "Princess Sure-E has no team:",
            {
                "age": None,
                "id": 5,
                "name": "Princess Sure-E",
                "secret_name": "Sure-E",
                "team_id": 3,
            },
        ],
        [
            "Deleted team:",
            {"headquarters": "Wakaland Capital City", "id": 3, "name": "Wakaland"},
        ],
    ]

    with pytest.raises(IntegrityError) as exc:
        mod.main()
    assert "FOREIGN KEY constraint failed" in str(exc.value)
