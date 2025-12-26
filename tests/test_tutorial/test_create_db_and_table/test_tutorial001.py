from pathlib import Path

import pytest

from ...conftest import coverage_run, needs_py310


@pytest.mark.parametrize(
    "module_name",
    [
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def test_create_db_and_table(cov_tmp_path: Path, module_name: str):
    module = f"docs_src.tutorial.create_db_and_table.{module_name}"
    result = coverage_run(module=module, cwd=cov_tmp_path)
    assert "BEGIN" in result.stdout
    assert 'PRAGMA main.table_info("hero")' in result.stdout
    assert "CREATE TABLE hero (" in result.stdout
    assert "id INTEGER NOT NULL," in result.stdout
    assert "name VARCHAR NOT NULL," in result.stdout
    assert "secret_name VARCHAR NOT NULL," in result.stdout
    assert "age INTEGER," in result.stdout
    assert "PRIMARY KEY (id)" in result.stdout
    assert ")" in result.stdout
    assert "COMMIT" in result.stdout
