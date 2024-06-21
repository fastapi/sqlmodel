import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine

from ....conftest import needs_py310


@needs_py310
def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.delete_records_relationship import (
        tutorial003_py310 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    with pytest.raises(IntegrityError):
        mod.main()
