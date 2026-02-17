import importlib

import pytest
from sqlalchemy import create_mock_engine
from sqlalchemy.sql.type_api import TypeEngine
from sqlmodel import SQLModel

from . import test_enums_models

"""
Tests related to Enums

Associated issues:
* https://github.com/tiangolo/sqlmodel/issues/96
* https://github.com/tiangolo/sqlmodel/issues/164
"""


def pg_dump(sql: TypeEngine, *args, **kwargs):
    dialect = sql.compile(dialect=postgres_engine.dialect)
    sql_str = str(dialect).rstrip()
    if sql_str:
        print(sql_str + ";")


def sqlite_dump(sql: TypeEngine, *args, **kwargs):
    dialect = sql.compile(dialect=sqlite_engine.dialect)
    sql_str = str(dialect).rstrip()
    if sql_str:
        print(sql_str + ";")


postgres_engine = create_mock_engine("postgresql://", pg_dump)
sqlite_engine = create_mock_engine("sqlite://", sqlite_dump)


def test_postgres_ddl_sql(clear_sqlmodel, capsys: pytest.CaptureFixture[str]):
    assert test_enums_models, "Ensure the models are imported and registered"
    importlib.reload(test_enums_models)
    SQLModel.metadata.create_all(bind=postgres_engine, checkfirst=False)

    captured = capsys.readouterr()
    assert "CREATE TYPE myenum1 AS ENUM ('A', 'B');" in captured.out
    assert "CREATE TYPE myenum2 AS ENUM ('C', 'D');" in captured.out


def test_sqlite_ddl_sql(clear_sqlmodel, capsys: pytest.CaptureFixture[str]):
    assert test_enums_models, "Ensure the models are imported and registered"
    importlib.reload(test_enums_models)
    SQLModel.metadata.create_all(bind=sqlite_engine, checkfirst=False)

    captured = capsys.readouterr()
    assert "enum_field VARCHAR(1) NOT NULL" in captured.out, captured
    assert "CREATE TYPE" not in captured.out


def test_json_schema_flat_model_pydantic_v2():
    assert test_enums_models.FlatModel.model_json_schema() == {
        "title": "FlatModel",
        "type": "object",
        "properties": {
            "id": {"title": "Id", "type": "string", "format": "uuid"},
            "enum_field": {"$ref": "#/$defs/MyEnum1"},
        },
        "required": ["id", "enum_field"],
        "$defs": {
            "MyEnum1": {"enum": ["A", "B"], "title": "MyEnum1", "type": "string"}
        },
    }


def test_json_schema_inherit_model_pydantic_v2():
    assert test_enums_models.InheritModel.model_json_schema() == {
        "title": "InheritModel",
        "type": "object",
        "properties": {
            "id": {"title": "Id", "type": "string", "format": "uuid"},
            "enum_field": {"$ref": "#/$defs/MyEnum2"},
        },
        "required": ["id", "enum_field"],
        "$defs": {
            "MyEnum2": {"enum": ["C", "D"], "title": "MyEnum2", "type": "string"}
        },
    }
