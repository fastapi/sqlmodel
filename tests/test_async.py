import asyncio
from typing import Generator, Optional

import pytest
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer


# The first time this test is run, it will download the postgres image which can take
# a while. Subsequent runs will be much faster.
@pytest.fixture(scope="module")
def postgres_container_url() -> Generator[str, None, None]:
    with PostgresContainer("postgres:13") as postgres:
        postgres.driver = "asyncpg"
        yield postgres.get_connection_url()


async def _test_async_create(postgres_container_url: str) -> None:
    class Hero(SQLModel, table=True):
        # SQLModel.metadata is a singleton and the Hero Class has already been defined.
        # If I flush the metadata during this test, it will cause test_enum to fail
        # because in that file, the model isn't defined within a function. For now, the
        # workaround is to set extend_existing to True. In the future, test setup and
        # teardown should be refactored to avoid this issue.
        __table_args__ = {"extend_existing": True}

        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None

    hero_create = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_async_engine(postgres_container_url)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        session.add(hero_create)
        await session.commit()
        await session.refresh(hero_create)

    async with AsyncSession(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = await session.exec(statement)
        hero_query = results.one()
        assert hero_create == hero_query


def test_async_create(postgres_container_url: str) -> None:
    asyncio.run(_test_async_create(postgres_container_url))
