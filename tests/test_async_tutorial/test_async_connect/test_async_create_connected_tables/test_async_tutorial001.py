import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_async_tutorial001()->None:
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


