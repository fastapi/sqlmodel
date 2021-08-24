from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from .main import app, get_session  # (1)


def test_create_hero():
    engine = create_engine(  # (2)
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)  # (3)

    with Session(engine) as session:  # (4)

        def get_session_override():
            return session  # (5)

        app.dependency_overrides[get_session] = get_session_override  # (4)

        client = TestClient(app)

        response = client.post(
            "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        )
        app.dependency_overrides.clear()
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Deadpond"
        assert data["secret_name"] == "Dive Wilson"
        assert data["age"] is None
        assert data["id"] is not None
    # (6)
