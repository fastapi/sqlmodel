import sys

import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

beforePYTHON3_9 = sys.version_info < (3, 9)
reasonPEP593 = "Annotations(PEP593 https://peps.python.org/pep-0593/) only compatible with Python ver >= 3.9"


@pytest.mark.skipif(beforePYTHON3_9, reason=reasonPEP593)
@pytest.mark.asyncio
async def test_async_tutorial001() -> None:
    from docs_src.tutorial_async.connect_async.create_tables_async import (
        tutorial001_async as mod,
    )

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)

    await mod.main()

    # Following code lines are for sync implementation , see following note regarding async
    # https://docs.sqlalchemy.org/en/14/errors.html#error-xd3s
    # insp: Inspector = inspect(mod.engine)
    # assert insp.has_table(str(mod.Hero.__tablename__))
    # assert insp.has_table(str(mod.Team.__tablename__))

    # following is recommended workaround
    async with mod.engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert str(mod.Team.__tablename__) in tables
    assert str(mod.Hero.__tablename__) in tables

    # TODO; work out how to call insp.has_tables  with run_sync
    # async with mod.engine.connect() as conn:
    #     insp: Inspector = await conn.run_sync(
    #         lambda sync_conn: inspect(sync_conn)
    #     )
    #     assert insp.has_table(str(mod.Hero.__tablename__))
    #     assert insp.has_table(str(mod.Team.__tablename__))
