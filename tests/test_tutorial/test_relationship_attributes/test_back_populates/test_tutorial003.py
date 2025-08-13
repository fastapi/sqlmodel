import importlib
import sys
import types
from typing import Any

import pytest
from sqlalchemy import inspect  # Keep this
from sqlalchemy.engine.reflection import Inspector  # Keep this
from sqlmodel import create_engine

from ....conftest import needs_py39, needs_py310  # Keep conftest imports


@pytest.fixture(
    name="module",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py39", marks=needs_py39),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def module_fixture(request: pytest.FixtureRequest, clear_sqlmodel: Any):
    module_name = request.param
    full_module_name = (
        f"docs_src.tutorial.relationship_attributes.back_populates.{module_name}"
    )

    if full_module_name in sys.modules:
        mod = importlib.reload(sys.modules[full_module_name])
    else:
        mod = importlib.import_module(full_module_name)

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    # This tutorial's main() function calls create_db_and_tables().
    # So, the fixture doesn't necessarily need to call SQLModel.metadata.create_all(mod.engine)
    # if main() is guaranteed to run and do it. However, for safety or if main() structure changes,
    # it can be included. Let's assume main() handles it as per typical tutorial structure.
    # If main() is *only* for data and not schema, then it's needed here.
    # The original test calls main() then inspects. So main must create tables.

    return mod


def test_tutorial(
    module: types.ModuleType, clear_sqlmodel: Any
):  # print_mock not needed
    # The main() function in the tutorial module is expected to create tables.
    module.main()

    insp: Inspector = inspect(module.engine)
    assert insp.has_table(str(module.Hero.__tablename__))
    assert insp.has_table(str(module.Weapon.__tablename__))  # Specific to tutorial003
    assert insp.has_table(str(module.Power.__tablename__))  # Specific to tutorial003
    assert insp.has_table(str(module.Team.__tablename__))
