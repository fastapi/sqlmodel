import enum
import uuid

from sqlalchemy import create_mock_engine
from sqlalchemy.sql.type_api import TypeEngine
from sqlmodel import Field, SQLModel

"""
Tests related to Enums

Associated issues:
* https://github.com/tiangolo/sqlmodel/issues/96
* https://github.com/tiangolo/sqlmodel/issues/164
"""


class MyEnum1(str, enum.Enum):
    A = "A"
    B = "B"


class MyEnum2(str, enum.Enum):
    C = "C"
    D = "D"


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum2


class FlatModel(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    enum_field: MyEnum1


class InheritModel(BaseModel, table=True):
    pass


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


def test_postgres_ddl_sql(capsys):
    SQLModel.metadata.create_all(bind=postgres_engine, checkfirst=False)

    captured = capsys.readouterr()
    assert "CREATE TYPE myenum1 AS ENUM ('A', 'B');" in captured.out
    assert "CREATE TYPE myenum2 AS ENUM ('C', 'D');" in captured.out


def test_sqlite_ddl_sql(capsys):
    SQLModel.metadata.create_all(bind=sqlite_engine, checkfirst=False)

    captured = capsys.readouterr()
    assert "enum_field VARCHAR(1) NOT NULL" in captured.out
    assert "CREATE TYPE" not in captured.out


def test_json_schema_flat_model():
    assert FlatModel.schema() == {
        "title": "FlatModel",
        "type": "object",
        "properties": {
            "id": {"title": "Id", "type": "string", "format": "uuid"},
            "enum_field": {"$ref": "#/definitions/MyEnum1"},
        },
        "required": ["id", "enum_field"],
        "definitions": {
            "MyEnum1": {
                "title": "MyEnum1",
                "description": "An enumeration.",
                "enum": ["A", "B"],
                "type": "string",
            }
        },
    }


def test_json_schema_inherit_model():
    assert InheritModel.schema() == {
        "title": "InheritModel",
        "type": "object",
        "properties": {
            "id": {"title": "Id", "type": "string", "format": "uuid"},
            "enum_field": {"$ref": "#/definitions/MyEnum2"},
        },
        "required": ["id", "enum_field"],
        "definitions": {
            "MyEnum2": {
                "title": "MyEnum2",
                "description": "An enumeration.",
                "enum": ["C", "D"],
                "type": "string",
            }
        },
    }
