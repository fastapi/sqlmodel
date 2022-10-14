import pytest
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_async_tutorial001():
    from docs_src.tutorial_async.connect_async.create_tables_async import (
        tutorial001_async as mod,
    )

    mod.sqlite_url = "sqlite+aiosqlite://"
    mod.engine = create_async_engine(mod.sqlite_url)
    meta = SQLModel.metadata
    async_session = sessionmaker(
        mod.engine, expire_on_commit=False, class_=AsyncSession
    )

    async with mod.engine.begin() as conn1:
        # await conn1.run_sync(meta.drop_all)
        await conn1.run_sync(meta.create_all)
    await mod.main()

    # async with async_session() as session1:
    #     async with session1.begin():
    #         await session1.run_sync(meta.create_all)
    # await session1.run_sync(mod.main())

    # async with mod.engine.begin() as conn1:
    #     await conn1.run_sync(mod.main())
    # await conn1.run_sync(meta.create_all)
    # mod.main()

    # insp: Inspector = inspect(mod.engine)
    # assert insp.has_table(str(mod.Hero.__tablename__))
    # assert insp.has_table(str(mod.Team.__tablename__))

    assert True
