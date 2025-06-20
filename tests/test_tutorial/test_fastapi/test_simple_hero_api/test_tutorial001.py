import importlib
import sys
import types
from typing import Any

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

from ....conftest import (
    needs_py310,  # This needs to be relative to this file's location
)


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = f"docs_src.tutorial.fastapi.simple_hero_api.{module_name}"

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    if not hasattr(mod, "connect_args"):
        mod.connect_args = {"check_same_thread": False}

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url, connect_args=mod.connect_args, poolclass=StaticPool
    )

    # This tutorial (simple_hero_api) also uses an app startup event to create tables.
    # So, explicit table creation here is not strictly needed if TestClient(mod.app) is used,
    # as it will trigger startup events.
    # SQLModel.metadata.create_all(mod.engine) # Or rely on app startup event

    return mod


def test_tutorial(
    module: types.ModuleType,
):  # clear_sqlmodel is implicitly used by get_module
    with TestClient(module.app) as client:
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000,  # This ID is part of the test logic for this tutorial specifically
        }
        response = client.post("/heroes/", json=hero1_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero1_data["name"]
        assert data["secret_name"] == hero1_data["secret_name"]
        assert data["id"] is not None
        assert data["age"] is None

        # For hero2, this tutorial expects the ID to be settable from the request
        # This is specific to this tutorial version, later tutorials might change this behavior
        response = client.post("/heroes/", json=hero2_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero2_data["name"]
        assert data["secret_name"] == hero2_data["secret_name"]
        assert data["id"] == hero2_data["id"], (
            "Up to this point it's still possible to "
            "set the ID of the hero in the request"
        )
        assert data["age"] is None

        response = client.get("/heroes/")
        data = response.json()

        assert response.status_code == 200, response.text
        assert len(data) == 2
        assert data[0]["name"] == hero1_data["name"]
        assert data[0]["secret_name"] == hero1_data["secret_name"]
        assert data[1]["name"] == hero2_data["name"]
        assert data[1]["secret_name"] == hero2_data["secret_name"]
        assert data[1]["id"] == hero2_data["id"]

        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        # The OpenAPI schema is expected to be consistent for both module versions
        assert response.json() == {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/heroes/": {
                    "get": {
                        "summary": "Read Heroes",
                        "operationId": "read_heroes_heroes__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                # For this tutorial, the response model for GET /heroes/ is not explicitly defined,
                                # so FastAPI/SQLModel might return a list of objects (dict).
                                # The original test had {"application/json": {"schema": {}}} which means any JSON.
                                # We'll keep it like that to match.
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    },
                    "post": {
                        "summary": "Create Hero",
                        "operationId": "create_hero_heroes__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Hero"}
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                # Similarly, POST /heroes/ response model is not explicitly defined in this tutorial.
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    },
                }
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                    "Hero": {
                        "title": "Hero",
                        "required": ["name", "secret_name"],
                        "type": "object",
                        "properties": {
                            "id": IsDict(
                                {
                                    "title": "Id",
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Id", "type": "integer"}
                            ),
                            "name": {"title": "Name", "type": "string"},
                            "secret_name": {"title": "Secret Name", "type": "string"},
                            "age": IsDict(
                                {
                                    "title": "Age",
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Age", "type": "integer"}
                            ),
                        },
                    },
                    "ValidationError": {
                        "title": "ValidationError",
                        "required": ["loc", "msg", "type"],
                        "type": "object",
                        "properties": {
                            "loc": {
                                "title": "Location",
                                "type": "array",
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                            },
                            "msg": {"title": "Message", "type": "string"},
                            "type": {"title": "Error Type", "type": "string"},
                        },
                    },
                }
            },
        }
