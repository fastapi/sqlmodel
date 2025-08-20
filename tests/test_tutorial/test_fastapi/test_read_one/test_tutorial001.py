import importlib
import sys
from types import ModuleType
from typing import Any

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
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
    module_name = f"docs_src.tutorial.fastapi.read_one.{request.param}"  # No .main
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    module.sqlite_url = "sqlite://"
    connect_args = getattr(module, "connect_args", {"check_same_thread": False})
    if "check_same_thread" not in connect_args:
        connect_args["check_same_thread"] = False

    module.engine = create_engine(
        module.sqlite_url, connect_args=connect_args, poolclass=StaticPool
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
            # id: 9000 was in original test, but usually not provided on create
        }
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text
        hero1 = response.json()  # Store created hero1 data

        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()  # Store created hero2 data

        response_get_all = client.get("/heroes/")
        assert response_get_all.status_code == 200, response_get_all.text
        data_all = response_get_all.json()
        assert len(data_all) == 2

        hero_id_to_get = hero2["id"]  # Use actual ID from created hero2
        response_get_one = client.get(f"/heroes/{hero_id_to_get}")
        assert response_get_one.status_code == 200, response_get_one.text
        data_one = response_get_one.json()
        assert data_one["name"] == hero2["name"]
        assert data_one["secret_name"] == hero2["secret_name"]
        assert data_one["age"] == hero2["age"]
        assert data_one["id"] == hero2["id"]

        # Check for a non-existent ID
        non_existent_id = hero1["id"] + hero2["id"] + 100  # A likely non-existent ID
        response_get_non_existent = client.get(f"/heroes/{non_existent_id}")
        assert response_get_non_existent.status_code == 404, (
            response_get_non_existent.text
        )

        response_openapi = client.get("/openapi.json")
        assert response_openapi.status_code == 200, response_openapi.text
        # OpenAPI schema check (remains the same as original)
        assert response_openapi.json() == {
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
                            }
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
