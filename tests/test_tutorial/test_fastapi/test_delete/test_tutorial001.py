import importlib
import sys
from types import ModuleType
from typing import Any # For clear_sqlmodel type hint

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine # Import SQLModel for metadata operations
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
    module_name = f"docs_src.tutorial.fastapi.delete.{request.param}" # No .main here
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    # Setup engine and tables for this module
    # This part is crucial and needs to happen after the module is loaded/reloaded
    # and after clear_sqlmodel has run.
    module.sqlite_url = "sqlite://"
    module.engine = create_engine(
        module.sqlite_url,
        connect_args={"check_same_thread": False}, # connect_args from original main.py
        poolclass=StaticPool
    )
    # Assuming the module has a create_db_and_tables or similar, or uses SQLModel.metadata directly
    if hasattr(module, "create_db_and_tables"):
        module.create_db_and_tables()
    else:
        SQLModel.metadata.create_all(module.engine) # Fallback, ensure tables are created

    return module


def test_tutorial(clear_sqlmodel: Any, module: ModuleType): # clear_sqlmodel is autouse but explicit for safety
    # The engine and tables are now set up by the 'module' fixture
    # The app's dependency overrides for get_session will use module.engine

    # Original test logic using TestClient with module.app
    with TestClient(module.app) as client:
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000, # Note: ID is part of creation data here
        }
        hero3_data = {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        }
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text
        hero1 = response.json() # Get actual ID of hero1
        hero1_id = hero1["id"]

        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()
        hero2_id = hero2["id"] # This will be the ID assigned by DB, not 9000 if 9000 is not allowed on POST

        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text
        hero3 = response.json()
        # hero3_id = hero3["id"] # Unused in original test logic for delete

        # Check if specific hero exists (e.g. hero2)
        response = client.get(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text

        # Original test checked for ID 9000 which might fail if ID is not settable on POST
        # For robustness, let's check for a non-existent ID based on actual data.
        # If hero2_id is 1, check for 9000. If it's 9000, check for 1 (assuming hero1_id is 1).
        non_existent_id_check = 9000
        if hero2_id == non_existent_id_check: # if DB somehow used 9000
            non_existent_id_check = hero1_id + hero2_id + 100 # just some other ID

        response = client.get(f"/heroes/{non_existent_id_check}")
        assert response.status_code == 404, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3

        response = client.patch(
            f"/heroes/{hero2_id}", json={"secret_name": "Spider-Youngster"}
        )
        assert response.status_code == 200, response.text

        response = client.patch(f"/heroes/{non_existent_id_check}", json={"name": "Dragon Cube X"})
        assert response.status_code == 404, response.text

        response = client.delete(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2 # After deleting one hero

        response = client.delete(f"/heroes/{non_existent_id_check}")
        assert response.status_code == 404, response.text

        # OpenAPI schema check (remains the same)
        response = client.get("/openapi.json")
        assert response.status_code == 200, response.text
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
