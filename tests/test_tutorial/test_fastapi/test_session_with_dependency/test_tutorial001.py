import importlib
import sys
import types
from typing import Any

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel
from sqlmodel.pool import StaticPool

from ....conftest import needs_py39, needs_py310


@pytest.fixture(
    name="module",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py39", marks=needs_py39),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = (
        f"docs_src.tutorial.fastapi.session_with_dependency.{module_name}"
    )

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    # Ensure connect_args is available in the module, default if not
    if not hasattr(mod, "connect_args"):
        mod.connect_args = {"check_same_thread": False}

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url, connect_args=mod.connect_args, poolclass=StaticPool
    )

    # The app needs the engine to be set before creating tables via startup event
    # In this tutorial, create_db_and_tables is called by a startup event handler in the app
    # So, we just need to ensure the engine is correctly assigned to the module.
    # SQLModel.metadata.create_all(mod.engine) might be redundant if app does it.
    # However, to be safe and cover cases where app might not do it, or for other tests,
    # it's often included. Given the tutorial structure, the app handles it.
    # For this specific tutorial, the app's startup event handles table creation.
    # mod.create_db_and_tables() is called within the app.on_event("startup")
    # So, explicit call here might be redundant or even cause issues if not idempotent.
    # Let's rely on the app's startup event as per the tutorial's design.
    # If `create_db_and_tables` exists as a global function in the module (outside app event), then call it.
    if hasattr(mod, "create_db_and_tables") and callable(mod.create_db_and_tables):
         # Check if it's the function that FastAPI would call, or a standalone one.
         # This tutorial series usually has `create_db_and_tables` called by `app.on_event("startup")`.
         # If the tests run TestClient(mod.app), startup events will run.
         pass # Assuming startup event handles it.

    return mod


def test_tutorial(module: types.ModuleType):
    # clear_sqlmodel is used by the get_module fixture
    with TestClient(module.app) as client:
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000, # This ID might be ignored by DB if it's auto-incrementing primary key
        }
        hero3_data = {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        }
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text

        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2_created = response.json() # Use the ID from the created hero
        hero2_id = hero2_created["id"]

        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text

        response = client.get(f"/heroes/{hero2_id}") # Use the actual ID from DB
        assert response.status_code == 200, response.text

        # If hero ID 9000 was intended to be a specific test case for a non-existent ID
        # after creating hero2 (which might get a different ID), this check is fine.
        # Otherwise, if hero2 was expected to have ID 9000, this needs adjustment.
        # Given typical auto-increment, ID 9000 for hero2 is unlikely unless DB is reset and hero2 is first entry.
        # The original test implies hero2_data's ID is not necessarily the created ID.
        response = client.get("/heroes/9000") # Check for a potentially non-existent ID
        assert response.status_code == 404, response.text # Expect 404 if 9000 is not hero2_id and not another hero's ID

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3

        response = client.patch(
            f"/heroes/{hero2_id}", json={"secret_name": "Spider-Youngster"}
        )
        assert response.status_code == 200, response.text

        response = client.patch("/heroes/9001", json={"name": "Dragon Cube X"}) # Non-existent ID
        assert response.status_code == 404, response.text

        response = client.delete(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2

        response = client.delete("/heroes/9000") # Non-existent ID (same as the GET check)
        assert response.status_code == 404, response.text

        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        # OpenAPI schema is expected to be consistent across these module versions
        assert response.json() == {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/heroes/": {
                    "get": {
                        "summary": "Read Heroes",
                        "operationId": "read_heroes_heroes__get",
                        "parameters": [
                            {
                                "required": False,
                                "schema": {
                                    "title": "Offset",
                                    "type": "integer",
                                    "default": 0,
                                },
                                "name": "offset",
                                "in": "query",
                            },
                            {
                                "required": False,
                                "schema": {
                                    "title": "Limit",
                                    "maximum": 100.0,
                                    "type": "integer",
                                    "default": 100,
                                },
                                "name": "limit",
                                "in": "query",
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Response Read Heroes Heroes  Get",
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/HeroPublic"
                                            },
                                        }
                                    }
                                },
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
                    "post": {
                        "summary": "Create Hero",
                        "operationId": "create_hero_heroes__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HeroCreate"
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HeroPublic"
                                        }
                                    }
                                },
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
                },
                "/heroes/{hero_id}": {
                    "get": {
                        "summary": "Read Hero",
                        "operationId": "read_hero_heroes__hero_id__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Hero Id", "type": "integer"},
                                "name": "hero_id",
                                "in": "path",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HeroPublic"
                                        }
                                    }
                                },
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
                    "delete": {
                        "summary": "Delete Hero",
                        "operationId": "delete_hero_heroes__hero_id__delete",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Hero Id", "type": "integer"},
                                "name": "hero_id",
                                "in": "path",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
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
                    "patch": {
                        "summary": "Update Hero",
                        "operationId": "update_hero_heroes__hero_id__patch",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Hero Id", "type": "integer"},
                                "name": "hero_id",
                                "in": "path",
                            }
                        ],
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HeroUpdate"
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HeroPublic"
                                        }
                                    }
                                },
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
                },
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
                    "HeroCreate": {
                        "title": "HeroCreate",
                        "required": ["name", "secret_name"],
                        "type": "object",
                        "properties": {
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
                    "HeroPublic": {
                        "title": "HeroPublic",
                        "required": ["name", "secret_name", "id"],
                        "type": "object",
                        "properties": {
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
                            "id": {"title": "Id", "type": "integer"},
                        },
                    },
                    "HeroUpdate": {
                        "title": "HeroUpdate",
                        "type": "object",
                        "properties": {
                            "name": IsDict(
                                {
                                    "title": "Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Name", "type": "string"}
                            ),
                            "secret_name": IsDict(
                                {
                                    "title": "Secret Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Secret Name", "type": "string"}
                            ),
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
