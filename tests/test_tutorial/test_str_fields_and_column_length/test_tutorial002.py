import importlib
import runpy
import sys
from collections.abc import Generator
from types import ModuleType
from unittest.mock import patch

import pytest
from sqlalchemy import create_mock_engine
from sqlalchemy.sql.type_api import TypeEngine
from sqlmodel import create_engine


def mysql_dump(sql: TypeEngine, *args, **kwargs):
    dialect = sql.compile(dialect=mysql_engine.dialect)
    sql_str = str(dialect).rstrip()
    if sql_str:
        print(sql_str + ";")


mysql_engine = create_mock_engine("mysql://", mysql_dump)


@pytest.fixture(
    name="mod",
    params=[
        "tutorial002_py310",
    ],
)
def get_module(request: pytest.FixtureRequest) -> Generator[ModuleType, None, None]:
    with patch("sqlmodel.create_engine"):  # To avoid "No module named 'MySQLdb'" error
        mod = importlib.import_module(
            f"docs_src.tutorial.str_fields_and_column_length.{request.param}"
        )
        yield mod


def test_sqlite_ddl_sql(mod: ModuleType, caplog: pytest.LogCaptureFixture):
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url, echo=True)
    mod.create_db_and_tables()
    assert "CREATE TABLE hero (" in caplog.text
    assert "name VARCHAR(100) NOT NULL" in caplog.text


def test_mysql_ddl_sql(mod: ModuleType, capsys: pytest.CaptureFixture[str]):
    importlib.reload(mod)

    mod.SQLModel.metadata.create_all(bind=mysql_engine, checkfirst=False)
    captured = capsys.readouterr()
    assert "CREATE TABLE hero (" in captured.out
    assert "name VARCHAR(100) NOT NULL" in captured.out


# For coverage
def test_run_main(mod: ModuleType):
    # Remove module to avoid double-import warning
    sys.modules.pop(mod.__name__, None)

    runpy.run_module(mod.__name__, run_name="__main__")
