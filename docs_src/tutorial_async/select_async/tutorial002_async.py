import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession  # (1)


class Hero(SQLModel, table=True):  # (2)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)  # (3)


async def create_db_and_tables():
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)  # (4)


async def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")  # (5)
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:  # (6)
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        await session.commit()


async def select_heroes():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:  # (7)
        statement = select(Hero)  # (8)
        results = await session.exec(statement)  # (9)
        for hero in results:  # (10)
            print(hero)  # (11)
    # (12)


async def main():
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()  # (13)


if __name__ == "__main__":
    asyncio.run(main)
