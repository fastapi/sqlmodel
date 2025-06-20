import importlib
import sys
from types import ModuleType
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine  # Keep this for session_fixture
from sqlmodel.pool import StaticPool  # Keep this for session_fixture

from ....conftest import needs_py39, needs_py310


# This will be our parametrized fixture providing the versioned 'main' module
@pytest.fixture(
    name="module",
    scope="function",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py39", marks=needs_py39),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(
    request: pytest.FixtureRequest, clear_sqlmodel: Any
) -> ModuleType:  # clear_sqlmodel is autouse
    module_name = f"docs_src.tutorial.fastapi.app_testing.{request.param}.main"

    # Forcing reload to try to get a fresh state for models
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)
    return module


@pytest.fixture(name="session", scope="function")
def session_fixture(module: ModuleType) -> Generator[Session, None, None]:
    # Store original engine-related attributes from the module
    original_engine = getattr(module, "engine", None)
    original_sqlite_url = getattr(module, "sqlite_url", None)
    original_connect_args = getattr(module, "connect_args", None)

    # Force module to use a fresh in-memory SQLite DB for this test run
    module.sqlite_url = "sqlite://"
    module.connect_args = {"check_same_thread": False}  # Crucial for FastAPI + SQLite

    # Re-create the engine in the module to use these new settings
    test_engine = create_engine(
        module.sqlite_url,
        connect_args=module.connect_args,
        poolclass=StaticPool,  # Recommended for tests
    )
    module.engine = test_engine

    if hasattr(module, "create_db_and_tables"):
        module.create_db_and_tables()  # This should use module.engine
    else:
        # Fallback if the function isn't named create_db_and_tables
        SQLModel.metadata.create_all(module.engine)

    with Session(
        module.engine
    ) as session:  # Use the module's (now test-configured) engine
        yield session

    # Teardown: drop tables from the module's engine
    SQLModel.metadata.drop_all(module.engine)

    # Restore original attributes if they existed
    if original_sqlite_url is not None:
        module.sqlite_url = original_sqlite_url
    if original_connect_args is not None:
        module.connect_args = original_connect_args
    if original_engine is not None:
        module.engine = original_engine
    else:  # If engine didn't exist, remove the one we created
        if hasattr(module, "engine"):
            del module.engine


@pytest.fixture(name="client", scope="function")
def client_fixture(
    session: Session, module: ModuleType
) -> Generator[TestClient, None, None]:
    def get_session_override() -> Generator[Session, None, None]:  # Must be a generator
        yield session

    module.app.dependency_overrides[module.get_session] = get_session_override

    test_client = TestClient(module.app)
    yield test_client

    module.app.dependency_overrides.clear()


def test_create_hero(client: TestClient, module: ModuleType):
    response = client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient, module: ModuleType):
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient, module: ModuleType):
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_heroes(session: Session, client: TestClient, module: ModuleType):
    # Use module.Hero for creating instances
    hero_1 = module.Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = module.Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id


def test_read_hero(session: Session, client: TestClient, module: ModuleType):
    hero_1 = module.Hero(name="Deadpond", secret_name="Dive Wilson")  # Use module.Hero
    session.add(hero_1)
    session.commit()

    response = client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id


def test_update_hero(session: Session, client: TestClient, module: ModuleType):
    hero_1 = module.Hero(name="Deadpond", secret_name="Dive Wilson")  # Use module.Hero
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] == hero_1.id


def test_delete_hero(session: Session, client: TestClient, module: ModuleType):
    hero_1 = module.Hero(name="Deadpond", secret_name="Dive Wilson")  # Use module.Hero
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(module.Hero, hero_1.id)  # Use module.Hero

    assert response.status_code == 200
    assert hero_in_db is None
