from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

openapi_schema = {
    "openapi": "3.0.2",
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
                                    "items": {"$ref": "#/components/schemas/HeroRead"},
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
                            "schema": {"$ref": "#/components/schemas/HeroCreate"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HeroRead"}
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
                        "items": {"$ref": "#/components/schemas/ValidationError"},
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
                    "age": {"title": "Age", "type": "integer"},
                },
            },
            "HeroRead": {
                "title": "HeroRead",
                "required": ["name", "secret_name", "id"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "secret_name": {"title": "Secret Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"},
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
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.fastapi.multiple_models import tutorial002 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url, connect_args=mod.connect_args, poolclass=StaticPool
    )

    with TestClient(mod.app) as client:
        hero1_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000,
        }
        response = client.post("/heroes/", json=hero1_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero1_data["name"]
        assert data["secret_name"] == hero1_data["secret_name"]
        assert data["id"] is not None
        assert data["age"] is None

        response = client.post("/heroes/", json=hero2_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero2_data["name"]
        assert data["secret_name"] == hero2_data["secret_name"]
        assert data["id"] != hero2_data["id"], (
            "Now it's not possible to predefine the ID from the request, "
            "it's now set by the database"
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
        assert data[1]["id"] != hero2_data["id"]

        response = client.get("/openapi.json")
        data = response.json()

        assert response.status_code == 200, response.text

        assert data == openapi_schema

    # Test inherited indexes
    insp: Inspector = inspect(mod.engine)
    indexes = insp.get_indexes(str(mod.Hero.__tablename__))
    expected_indexes = [
        {
            "name": "ix_hero_age",
            "dialect_options": {},
            "column_names": ["age"],
            "unique": 0,
        },
        {
            "name": "ix_hero_name",
            "dialect_options": {},
            "column_names": ["name"],
            "unique": 0,
        },
    ]
    for index in expected_indexes:
        assert index in indexes, "This expected index should be in the indexes in DB"
        # Now that this index was checked, remove it from the list of indexes
        indexes.pop(indexes.index(index))
    assert len(indexes) == 0, "The database should only have the expected indexes"
