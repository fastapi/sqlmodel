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
    from docs_src.tutorial.fastapi.read_one import tutorial001 as mod

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
        assert response.status_code == 200, response.text
        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()
        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2

        hero_id = hero2["id"]
        response = client.get(f"/heroes/{hero_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == hero2

        response = client.get("/heroes/9000")
        assert response.status_code == 404, response.text

        response = client.get("/openapi.json")
        data = response.json()

        assert response.status_code == 200, response.text

        # assert data == openapi_schema
