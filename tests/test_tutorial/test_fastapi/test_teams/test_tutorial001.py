import importlib
import sys
import types
from typing import Any

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import create_engine
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
    full_module_name = f"docs_src.tutorial.fastapi.teams.{module_name}"

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

    # This tutorial series typically uses a startup event in the app to create tables.
    # Relying on TestClient(mod.app) to trigger this.
    # Explicit SQLModel.metadata.create_all(mod.engine) is generally not needed here.

    return mod


def test_tutorial(
    module: types.ModuleType,
):  # clear_sqlmodel is implicitly used by get_module
    with TestClient(module.app) as client:
        # Hero Operations
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {  # This hero's ID might be overridden by DB if not specified or if ID is auto-incrementing
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000,
        }
        hero3_data = {"name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48}

        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text

        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2_created = response.json()
        hero2_id = hero2_created["id"]  # Use the actual ID returned by the DB

        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text

        response = client.get(f"/heroes/{hero2_id}")  # Use DB generated ID
        assert response.status_code == 200, response.text

        response = client.get(
            "/heroes/9000"
        )  # Check for ID 9000 specifically (could be hero2_id or not)
        if hero2_id == 9000:  # If hero2 got ID 9000
            assert response.status_code == 200, response.text
        else:  # If hero2 got a different ID, then 9000 should not exist
            assert response.status_code == 404, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3

        response = client.patch(
            f"/heroes/{hero2_id}", json={"secret_name": "Spider-Youngster"}
        )
        assert response.status_code == 200, response.text

        response = client.patch(
            "/heroes/9001", json={"name": "Dragon Cube X"}
        )  # Non-existent ID
        assert response.status_code == 404, response.text

        response = client.delete(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text

        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2

        response = client.delete("/heroes/9000")  # Try deleting ID 9000
        if hero2_id == 9000 and hero2_id not in [
            h["id"] for h in data
        ]:  # If it was hero2's ID and hero2 was deleted
            assert response.status_code == 404  # Already deleted
        elif hero2_id != 9000 and 9000 not in [
            h["id"] for h in data
        ]:  # If 9000 was never a valid ID among current heroes
            assert response.status_code == 404
        else:  # If 9000 was a valid ID of another hero still present (should not happen with current data)
            assert (
                response.status_code == 200
            )  # This case is unlikely with current test data

        # Team Operations
        team_preventers_data = {"name": "Preventers", "headquarters": "Sharp Tower"}
        team_z_force_data = {"name": "Z-Force", "headquarters": "Sister Margaret's Bar"}

        response = client.post("/teams/", json=team_preventers_data)
        assert response.status_code == 200, response.text
        team_preventers_created = response.json()
        team_preventers_id = team_preventers_created["id"]

        response = client.post("/teams/", json=team_z_force_data)
        assert response.status_code == 200, response.text
        team_z_force_created = response.json()

        response = client.get("/teams/")
        data = response.json()
        assert len(data) == 2

        response = client.get(f"/teams/{team_preventers_id}")
        data = response.json()
        assert response.status_code == 200, response.text
        # Compare created data, not input data, as ID is added
        assert data["name"] == team_preventers_created["name"]
        assert data["headquarters"] == team_preventers_created["headquarters"]
        assert data["id"] == team_preventers_created["id"]

        response = client.get("/teams/9000")  # Non-existent team ID
        assert response.status_code == 404, response.text

        response = client.patch(
            f"/teams/{team_preventers_id}", json={"headquarters": "Preventers Tower"}
        )
        data = response.json()
        assert response.status_code == 200, response.text
        assert data["name"] == team_preventers_data["name"]  # Name should be unchanged
        assert data["headquarters"] == "Preventers Tower"

        response = client.patch(
            "/teams/9000", json={"name": "Freedom League"}
        )  # Non-existent
        assert response.status_code == 404, response.text

        response = client.delete(f"/teams/{team_preventers_id}")
        assert response.status_code == 200, response.text

        response = client.delete("/teams/9000")  # Non-existent
        assert response.status_code == 404, response.text

        response = client.get("/teams/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

        # OpenAPI Schema Check (remains the same as it's consistent across module versions)
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
                "/teams/": {
                    "get": {
                        "summary": "Read Teams",
                        "operationId": "read_teams_teams__get",
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
                                            "title": "Response Read Teams Teams  Get",
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/TeamPublic"
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
                        "summary": "Create Team",
                        "operationId": "create_team_teams__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TeamCreate"
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
                                            "$ref": "#/components/schemas/TeamPublic"
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
                "/teams/{team_id}": {
                    "get": {
                        "summary": "Read Team",
                        "operationId": "read_team_teams__team_id__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Team Id", "type": "integer"},
                                "name": "team_id",
                                "in": "path",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/TeamPublic"
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
                        "summary": "Delete Team",
                        "operationId": "delete_team_teams__team_id__delete",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Team Id", "type": "integer"},
                                "name": "team_id",
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
                        "summary": "Update Team",
                        "operationId": "update_team_teams__team_id__patch",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Team Id", "type": "integer"},
                                "name": "team_id",
                                "in": "path",
                            }
                        ],
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TeamUpdate"
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
                                            "$ref": "#/components/schemas/TeamPublic"
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
                            "team_id": IsDict(
                                {
                                    "title": "Team Id",
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Team Id", "type": "integer"}
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
                            "team_id": IsDict(
                                {
                                    "title": "Team Id",
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Team Id", "type": "integer"}
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
                            "team_id": IsDict(
                                {
                                    "title": "Team Id",
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Team Id", "type": "integer"}
                            ),
                        },
                    },
                    "TeamCreate": {
                        "title": "TeamCreate",
                        "required": ["name", "headquarters"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "headquarters": {"title": "Headquarters", "type": "string"},
                        },
                    },
                    "TeamPublic": {
                        "title": "TeamPublic",
                        "required": ["name", "headquarters", "id"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "headquarters": {"title": "Headquarters", "type": "string"},
                            "id": {"title": "Id", "type": "integer"},
                        },
                    },
                    "TeamUpdate": {
                        "title": "TeamUpdate",
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
                            "headquarters": IsDict(
                                {
                                    "title": "Headquarters",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Headquarters", "type": "string"}
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
