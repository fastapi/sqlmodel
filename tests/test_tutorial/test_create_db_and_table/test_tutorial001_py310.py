from pathlib import Path

from ...conftest import coverage_run, needs_py310


@needs_py310
def test_create_db_and_table(cov_tmp_path: Path):
    module = "docs_src.tutorial.create_db_and_table.tutorial001_py310"
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
