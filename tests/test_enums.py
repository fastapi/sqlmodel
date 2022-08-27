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


class MyEnum1(enum.Enum):
    A = "A"
    B = "B"


class MyEnum2(enum.Enum):
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
