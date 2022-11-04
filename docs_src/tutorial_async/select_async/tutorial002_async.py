import asyncio
from typing import Annotated, Optional

# TODO change when https://github.com/tiangolo/sqlmodel/pull/435 accepted
# TODO replace following 3 lines with:
# ------ from sqlmodel import AsyncSession, create_async_engine, Field, SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession  # (1)


class Hero(SQLModel, table=True):  # (2)
    id: Annotated[int, Field(primary_key=True)]
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)  # (3)


async def create_db_and_tables() -> None:
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)  # (4)


async def create_heroes() -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  # (5)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    async with AsyncSession(engine) as session:  # (6)
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        await session.commit()


async def select_heroes() -> None:
    async with AsyncSession(engine) as session:  # (7)
        statement = select(Hero)  # (8)
        results = await session.exec(statement)  # (9)
        for hero in results:  # (10)
            print(hero)  # (11)
    # (12)


async def main() -> None:
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()  # (13)


if __name__ == "__main__":
    asyncio.run(main())
