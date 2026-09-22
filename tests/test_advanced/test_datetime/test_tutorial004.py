import importlib
from io import StringIO
from types import ModuleType

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial004_py310"),
    ],
)
def get_module(request: pytest.FixtureRequest) -> ModuleType:
    return importlib.import_module(f"docs_src.advanced.datetime.{request.param}")


def test_tutorial(mod: ModuleType) -> None:
    output = StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={"as_sql": True, "output_buffer": output},
    )
    with Operations.context(context):
        mod.upgrade()
        mod.downgrade()

    assert output.getvalue() == (
        "ALTER TABLE event ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE "
        "USING created_at AT TIME ZONE 'UTC';\n\n"
        "ALTER TABLE event ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE "
        "USING created_at AT TIME ZONE 'UTC';\n\n"
    )
