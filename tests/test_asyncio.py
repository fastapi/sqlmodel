import asyncio
from collections.abc import Mapping
from typing import Any

import pytest
from sqlalchemy import update
from sqlalchemy.engine import CursorResult, ScalarResult
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel, col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import Unpack, assert_type


@pytest.mark.parametrize("execution_options", [{}, {"populate_existing": True}])
def test_async_session(execution_options: Mapping[str, Any]) -> None:
    class Hero(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str

    async def run() -> None:
        engine = create_async_engine("sqlite+aiosqlite://")
        try:
            async with engine.begin() as connection:
                await connection.run_sync(SQLModel.metadata.create_all)
            async with AsyncSession(engine) as session:
                session.add(Hero(name="Deadpond"))
                await session.commit()

                statement = select(Hero)
                result = await session.exec(
                    statement, execution_options=execution_options
                )
                assert_type(result, ScalarResult[Hero])
                assert result.one().name == "Deadpond"

                with pytest.warns(DeprecationWarning, match="session.exec"):
                    scalars = await session.scalars(statement)
                assert_type(scalars, ScalarResult[Hero])
                assert scalars.one().name == "Deadpond"

                row = (await session.exec(select(col(Hero.id), Hero.name))).one()
                assert_type(row, tuple[int | None, str])
                assert row == (1, "Deadpond")

                updated = await session.exec(update(Hero).values(name="Rusty-Man"))
                assert_type(updated, CursorResult[Unpack[tuple[Any, ...]]])
                assert updated.rowcount == 1
                await session.commit()
                assert (await session.exec(select(Hero.name))).one() == "Rusty-Man"

                with pytest.warns(DeprecationWarning, match="session.exec"):
                    result = await session.execute(select(Hero))  # ty: ignore[deprecated]
                assert result.scalars().one().name == "Rusty-Man"
        finally:
            await engine.dispose()

    asyncio.run(run())
