import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.relationship_attributes.delete_records_relationship import (
        tutorial003 as mod,
    )

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)

    with pytest.raises(IntegrityError):
        mod.main()
