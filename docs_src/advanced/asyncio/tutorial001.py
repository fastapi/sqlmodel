import asyncio
from typing import Optional

from sqlmodel import AsyncSession, Field, SQLModel, create_async_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_and_tables():
    async with engine.begin() as session:
        await session.run_sync(SQLModel.metadata.create_all)


async def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    session = AsyncSession(engine)
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)

    await session.commit()

    await session.close()


async def select_heroes():
    async with AsyncSession(engine) as session:
        statement = select(Hero)
        results = await session.exec(statement)
        for hero in results:
            print(hero)


async def main():
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()


if __name__ == "__main__":
    asyncio.run(main())
