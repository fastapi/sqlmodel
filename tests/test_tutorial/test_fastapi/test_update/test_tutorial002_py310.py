from dirty_equals import IsDict
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from ....conftest import needs_py310


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.fastapi.update import tutorial002_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url, connect_args=mod.connect_args, poolclass=StaticPool
    )

    with TestClient(mod.app) as client:
        hero1_data = {
            "name": "Deadpond",
            "secret_name": "Dive Wilson",
            "password": "chimichanga",
        }
        hero2_data = {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "id": 9000,
            "password": "auntmay",
        }
        hero3_data = {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
            "password": "bestpreventer",
        }
        response = client.post("/heroes/", json=hero1_data)
        assert response.status_code == 200, response.text
        hero1 = response.json()
        assert "password" not in hero1
        assert "hashed_password" not in hero1
        hero1_id = hero1["id"]
        response = client.post("/heroes/", json=hero2_data)
        assert response.status_code == 200, response.text
        hero2 = response.json()
        hero2_id = hero2["id"]
        response = client.post("/heroes/", json=hero3_data)
        assert response.status_code == 200, response.text
        hero3 = response.json()
        hero3_id = hero3["id"]
        response = client.get(f"/heroes/{hero2_id}")
        assert response.status_code == 200, response.text
        fetched_hero2 = response.json()
        assert "password" not in fetched_hero2
        assert "hashed_password" not in fetched_hero2
        response = client.get("/heroes/9000")
        assert response.status_code == 404, response.text
        response = client.get("/heroes/")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3
        for response_hero in data:
            assert "password" not in response_hero
            assert "hashed_password" not in response_hero

        # Test hashed passwords
        with Session(mod.engine) as session:
            hero1_db = session.get(mod.Hero, hero1_id)
            assert hero1_db
            assert not hasattr(hero1_db, "password")
            assert hero1_db.hashed_password == "not really hashed chimichanga hehehe"
            hero2_db = session.get(mod.Hero, hero2_id)
            assert hero2_db
            assert not hasattr(hero2_db, "password")
            assert hero2_db.hashed_password == "not really hashed auntmay hehehe"
            hero3_db = session.get(mod.Hero, hero3_id)
            assert hero3_db
            assert not hasattr(hero3_db, "password")
            assert hero3_db.hashed_password == "not really hashed bestpreventer hehehe"

        response = client.patch(
            f"/heroes/{hero2_id}", json={"secret_name": "Spider-Youngster"}
        )
        data = response.json()
        assert response.status_code == 200, response.text
        assert data["name"] == hero2_data["name"], "The name should not be set to none"
        assert data["secret_name"] == "Spider-Youngster", (
            "The secret name should be updated"
        )
        assert "password" not in data
        assert "hashed_password" not in data
        with Session(mod.engine) as session:
            hero2b_db = session.get(mod.Hero, hero2_id)
            assert hero2b_db
            assert not hasattr(hero2b_db, "password")
            assert hero2b_db.hashed_password == "not really hashed auntmay hehehe"

        response = client.patch(f"/heroes/{hero3_id}", json={"age": None})
        data = response.json()
        assert response.status_code == 200, response.text
        assert data["name"] == hero3_data["name"]
        assert data["age"] is None, (
            "A field should be updatable to None, even if that's the default"
        )
        assert "password" not in data
        assert "hashed_password" not in data
        with Session(mod.engine) as session:
            hero3b_db = session.get(mod.Hero, hero3_id)
            assert hero3b_db
            assert not hasattr(hero3b_db, "password")
            assert hero3b_db.hashed_password == "not really hashed bestpreventer hehehe"

        # Test update dict, hashed_password
        response = client.patch(
            f"/heroes/{hero3_id}", json={"password": "philantroplayboy"}
        )
        data = response.json()
        assert response.status_code == 200, response.text
        assert data["name"] == hero3_data["name"]
        assert data["age"] is None
        assert "password" not in data
        assert "hashed_password" not in data
        with Session(mod.engine) as session:
            hero3b_db = session.get(mod.Hero, hero3_id)
            assert hero3b_db
            assert not hasattr(hero3b_db, "password")
            assert (
                hero3b_db.hashed_password == "not really hashed philantroplayboy hehehe"
            )

        response = client.patch("/heroes/9001", json={"name": "Dragon Cube X"})
        assert response.status_code == 404, response.text

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
                                    "maximum": 100,
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
                        "required": ["name", "secret_name", "password"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "secret_name": {"title": "Secret Name", "type": "string"},
                            "age": IsDict(
                                {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Age",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
                                {"title": "Age", "type": "integer"}
                            ),
                            "password": {"type": "string", "title": "Password"},
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
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Age",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
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
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Name",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
                                {"title": "Name", "type": "string"}
                            ),
                            "secret_name": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Secret Name",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
                                {"title": "Secret Name", "type": "string"}
                            ),
                            "age": IsDict(
                                {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Age",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
                                {"title": "Age", "type": "integer"}
                            ),
                            "password": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Password",
                                }
                            )
                            | IsDict(
                                # TODO: Remove when deprecating Pydantic v1
                                {"title": "Password", "type": "string"}
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
