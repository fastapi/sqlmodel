from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ...conftest import needs_py310


@needs_py310
def test_create_db_and_table(clear_sqlmodel):
    from docs_src.tutorial.create_db_and_table import tutorial003_py310 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    mod.create_db_and_tables()
    insp: Inspector = inspect(mod.engine)
    assert insp.has_table(str(mod.Hero.__tablename__))
