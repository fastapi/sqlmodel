from fastapi.testclient import TestClient
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
                                    "items": {"$ref": "#/components/schemas/Hero"},
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
                            "schema": {"$ref": "#/components/schemas/Hero"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Hero"}
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
            "Hero": {
                "title": "Hero",
                "required": ["name", "secret_name"],
                "type": "object",
                "properties": {
                    "id": {"title": "Id", "type": "integer"},
                    "name": {"title": "Name", "type": "string"},
                    "secret_name": {"title": "Secret Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"},
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
    from docs_src.tutorial.fastapi.response_model import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url, connect_args=mod.connect_args, poolclass=StaticPool
    )

    with TestClient(mod.app) as client:

        hero_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
        response = client.post("/heroes/", json=hero_data)
        data = response.json()

        assert response.status_code == 200, response.text
        assert data["name"] == hero_data["name"]
        assert data["secret_name"] == hero_data["secret_name"]
        assert data["id"] is not None
        assert data["age"] is None

        response = client.get("/heroes/")
        data = response.json()

        assert response.status_code == 200, response.text
        assert len(data) == 1
        assert data[0]["name"] == hero_data["name"]
        assert data[0]["secret_name"] == hero_data["secret_name"]

        response = client.get("/openapi.json")
        data = response.json()

        assert response.status_code == 200, response.text

        # assert data == openapi_schema
