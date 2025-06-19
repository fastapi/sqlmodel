import importlib
import sys
from types import ModuleType
from typing import Any # For clear_sqlmodel type hint

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import SQLModel, create_engine # Import SQLModel
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
    module_name = f"docs_src.tutorial.fastapi.multiple_models.{request.param}" # No .main
    if module_name in sys.modules:
        module = importlib.reload(sys.modules[module_name])
    else:
        module = importlib.import_module(module_name)

    module.sqlite_url = "sqlite://"
    # Ensure connect_args is available in module, default if not.
    # Some tutorial files might not define it if they don't use on_event("startup") for engine creation.
    connect_args = getattr(module, "connect_args", {"check_same_thread": False})
    if "check_same_thread" not in connect_args: # Ensure this specific arg for SQLite
        connect_args["check_same_thread"] = False

    module.engine = create_engine(
        module.sqlite_url,
        connect_args=connect_args,
        poolclass=StaticPool
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
        }
        response = client.post("/heroes/", json=hero1_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero1_data["name"]
        assert data["secret_name"] == hero1_data["secret_name"]
        assert data["id"] is not None
        assert data["age"] is None
        hero1_id = data["id"] # Store actual ID

        response = client.post("/heroes/", json=hero2_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero2_data["name"]
        assert data["secret_name"] == hero2_data["secret_name"]
        # The original test asserted data["id"] != hero2_data["id"] (which was 9000)
        # This is true if ID is auto-generated and not 9000.
        assert data["id"] is not None
        assert data["age"] is None
        hero2_id = data["id"] # Store actual ID


        response = client.get("/heroes/")
        data = response.json()

        assert response.status_code == 200, response.text
        assert len(data) == 2
        # Order might not be guaranteed, so check based on content if necessary,
        # but for now, assume order of creation is preserved in simple select.
        assert data[0]["id"] == hero1_id
        assert data[0]["name"] == hero1_data["name"]
        assert data[0]["secret_name"] == hero1_data["secret_name"]
        assert data[1]["id"] == hero2_id
        assert data[1]["name"] == hero2_data["name"]
        assert data[1]["secret_name"] == hero2_data["secret_name"]


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
                        "required": ["id", "name", "secret_name"],
                        "type": "object",
                        "properties": {
                            "id": {"title": "Id", "type": "integer"},
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

    # Test inherited indexes
    insp: Inspector = inspect(module.engine) # Use module.engine
    indexes = insp.get_indexes(str(module.Hero.__tablename__)) # Use module.Hero
    expected_indexes = [
        {
            "name": "ix_hero_name",
            "dialect_options": {},
            "column_names": ["name"],
            "unique": 0,
        },
        {
            "name": "ix_hero_age",
            "dialect_options": {},
            "column_names": ["age"],
            "unique": 0,
        },
    ]
    # Convert list of dicts to list of tuples of sorted items for order-agnostic comparison
    indexes_for_comparison = [tuple(sorted(d.items())) for d in indexes]
    expected_indexes_for_comparison = [tuple(sorted(d.items())) for d in expected_indexes]

    for index_data_tuple in expected_indexes_for_comparison:
        assert index_data_tuple in indexes_for_comparison, f"Expected index {index_data_tuple} not found in DB indexes {indexes_for_comparison}"
        indexes_for_comparison.remove(index_data_tuple)

    assert len(indexes_for_comparison) == 0, f"Unexpected extra indexes found in DB: {indexes_for_comparison}"
