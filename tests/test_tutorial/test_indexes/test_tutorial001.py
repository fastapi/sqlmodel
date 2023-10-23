from unittest.mock import patch

from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlmodel import create_engine

from ...conftest import get_testing_print_function


def test_tutorial(clear_sqlmodel):
    from docs_src.tutorial.indexes import tutorial001 as mod

    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(mod.sqlite_url)
    calls = []

    new_print = get_testing_print_function(calls)

    with patch("builtins.print", new=new_print):
        mod.main()
    assert calls == [
        [{"secret_name": "Dive Wilson", "age": None, "id": 1, "name": "Deadpond"}]
    ]

    insp: Inspector = inspect(mod.engine)
    indexes = insp.get_indexes(str(mod.Hero.__tablename__))
    expected_indexes = [
        {
            "name": "ix_hero_name",
            "dialect_options": {},
            "column_names": ["name"],
            "unique": 0,
        },
        {
            "name": "ix_hero_age",
            "dialect_options": {},
            "column_names": ["age"],
            "unique": 0,
        },
    ]
    for index in expected_indexes:
        assert index in indexes, "This expected index should be in the indexes in DB"
        # Now that this index was checked, remove it from the list of indexes
        indexes.pop(indexes.index(index))
    assert len(indexes) == 0, "The database should only have the expected indexes"
