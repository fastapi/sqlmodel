from fastapi.testclient import TestClient
from sqlalchemy import Inspector, inspect
from sqlmodel import Session, create_engine

from . import main as app_mod
from .test_main import client_fixture, session_fixture

assert client_fixture, "This keeps the client fixture used below"
assert session_fixture, "This keeps the session fixture used by client_fixture"


def test_startup():
    app_mod.engine = create_engine("sqlite://")
    app_mod.on_startup()
    insp: Inspector = inspect(app_mod.engine)
    assert insp.has_table(str(app_mod.Hero.__tablename__))


def test_get_session():
    app_mod.engine = create_engine("sqlite://")
    for session in app_mod.get_session():
        assert isinstance(session, Session)
        assert session.bind == app_mod.engine


def test_read_hero_not_found(client: TestClient):
    response = client.get("/heroes/9000")
    assert response.status_code == 404


def test_update_hero_not_found(client: TestClient):
    response = client.patch("/heroes/9000", json={"name": "Very-Rusty-Man"})
    assert response.status_code == 404


def test_delete_hero_not_found(client: TestClient):
    response = client.delete("/heroes/9000")
    assert response.status_code == 404
