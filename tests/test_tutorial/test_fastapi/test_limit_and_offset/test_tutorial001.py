import importlib
import sys
from types import ModuleType
from typing import Any  # For clear_sqlmodel type hint

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine  # Import SQLModel for metadata operations
from sqlmodel.pool import StaticPool

from ....conftest import needs_py39, needs_py310


@pytest.fixture(
    name="module",
    scope="function",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py39", marks=needs_py39),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest, clear_sqlmodel: Any) -> ModuleType:
    module_name = (
        f"docs_src.tutorial.fastapi.limit_and_offset.{request.param}"  # No .main
    )
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    module.sqlite_url = "sqlite://"
    module.engine = create_engine(
        module.sqlite_url,
        connect_args={
            "check_same_thread": False
        },  # Assuming connect_args was in original mod or default
        poolclass=StaticPool,
    )
    if hasattr(module, "create_db_and_tables"):
        module.create_db_and_tables()
    else:
        SQLModel.metadata.create_all(module.engine)

    return module


def test_tutorial(clear_sqlmodel: Any, module: ModuleType):
    with TestClient(module.app) as client:
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            # Original test data included "id": 9000, but this is usually not provided on create
            # If the app allows client-settable ID on create, it can be added back.
            # For now, assuming ID is auto-generated.
        }
        hero3_data = {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        }
        # Create hero 1
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text
        hero1 = response.json()

        # Create hero 2
        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()
        hero2_id = hero2["id"]  # Use the actual ID from response

        # Create hero 3
        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text
        hero3 = response.json()

        # Check specific hero (hero2)
        response = client.get(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text

        # Check a non-existent ID (original test used 9000, adjust if necessary)
        # This assumes 9000 is not a valid ID after creating 3 heroes.
        # A more robust way would be to ensure the ID doesn't exist.
        response = client.get("/heroes/9000")
        assert response.status_code == 404, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3

        response = client.get("/heroes/", params={"limit": 2})
        assert response.status_code == 200, response.text
        data_limit2 = response.json()
        assert len(data_limit2) == 2
        assert (
            data_limit2[0]["name"] == hero1["name"]
        )  # Compare with actual created hero data
        assert data_limit2[1]["name"] == hero2["name"]

        response = client.get("/heroes/", params={"offset": 1})
        assert response.status_code == 200, response.text
        data_offset1 = response.json()
        assert len(data_offset1) == 2
        assert data_offset1[0]["name"] == hero2["name"]
        assert data_offset1[1]["name"] == hero3["name"]

        response = client.get("/heroes/", params={"offset": 1, "limit": 1})
        assert response.status_code == 200, response.text
        data_offset_limit = response.json()
        assert len(data_offset_limit) == 1
        assert data_offset_limit[0]["name"] == hero2["name"]

        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
        # OpenAPI schema check - kept as is from original test
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
                    }
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
