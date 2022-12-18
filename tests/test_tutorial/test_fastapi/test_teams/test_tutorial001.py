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
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Offset", "type": "integer", "default": 0},
                        "name": "offset",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {
                            "title": "Limit",
                            "type": "integer",
                            "default": 100,
                            "lte": 100,
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
                                    "items": {"$ref": "#/components/schemas/HeroRead"},
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
                            "schema": {"$ref": "#/components/schemas/HeroUpdate"}
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
        "/teams/": {
            "get": {
                "summary": "Read Teams",
                "operationId": "read_teams_teams__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Offset", "type": "integer", "default": 0},
                        "name": "offset",
                        "in": "query",
                    },
                    {
                        "required": False,
                        "schema": {
                            "title": "Limit",
                            "type": "integer",
                            "default": 100,
                            "lte": 100,
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
                                    "items": {"$ref": "#/components/schemas/TeamRead"},
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
                            "schema": {"$ref": "#/components/schemas/TeamCreate"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TeamRead"}
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
                                "schema": {"$ref": "#/components/schemas/TeamRead"}
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
                            "schema": {"$ref": "#/components/schemas/TeamUpdate"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TeamRead"}
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
                    "team_id": {"title": "Team Id", "type": "integer"},
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
                    "team_id": {"title": "Team Id", "type": "integer"},
                    "id": {"title": "Id", "type": "integer"},
                },
            },
            "HeroUpdate": {
                "title": "HeroUpdate",
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "secret_name": {"title": "Secret Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"},
                    "team_id": {"title": "Team Id", "type": "integer"},
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
            "TeamRead": {
                "title": "TeamRead",
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
                    "name": {"title": "Name", "type": "string"},
                    "headquarters": {"title": "Headquarters", "type": "string"},
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
    from docs_src.tutorial.fastapi.teams import tutorial001 as mod

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
        hero3_data = {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
        }
        response = client.get("/openapi.json")
        data = response.json()
        assert response.status_code == 200, response.text
        # assert data == openapi_schema
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text
        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()
        hero2_id = hero2["id"]
        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text
        response = client.get(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text
        response = client.get("/heroes/9000")
        assert response.status_code == 404, response.text
        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3
        response = client.patch(
            f"/heroes/{hero2_id}", json={"secret_name": "Spider-Youngster"}
        )
        assert response.status_code == 200, response.text
        response = client.patch("/heroes/9001", json={"name": "Dragon Cube X"})
        assert response.status_code == 404, response.text
        response = client.delete(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text
        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2
        response = client.delete("/heroes/9000")
        assert response.status_code == 404, response.text

        team_preventers = {"name": "Preventers", "headquarters": "Sharp Tower"}
        team_z_force = {"name": "Z-Force", "headquarters": "Sister Margaret’s Bar"}
        response = client.post("/teams/", json=team_preventers)
        assert response.status_code == 200, response.text
        team_preventers_data = response.json()
        team_preventers_id = team_preventers_data["id"]
        response = client.post("/teams/", json=team_z_force)
        assert response.status_code == 200, response.text
        team_z_force_data = response.json()
        team_z_force_data["id"]
        response = client.get("/teams/")
        data = response.json()
        assert len(data) == 2
        response = client.get(f"/teams/{team_preventers_id}")
        data = response.json()
        assert response.status_code == 200, response.text
        assert data == team_preventers_data
        response = client.get("/teams/9000")
        assert response.status_code == 404, response.text
        response = client.patch(
            f"/teams/{team_preventers_id}", json={"headquarters": "Preventers Tower"}
        )
        data = response.json()
        assert response.status_code == 200, response.text
        assert data["name"] == team_preventers["name"]
        assert data["headquarters"] == "Preventers Tower"
        response = client.patch("/teams/9000", json={"name": "Freedom League"})
        assert response.status_code == 404, response.text
        response = client.delete(f"/teams/{team_preventers_id}")
        assert response.status_code == 200, response.text
        response = client.delete("/teams/9000")
        assert response.status_code == 404, response.text
        response = client.get("/teams/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
