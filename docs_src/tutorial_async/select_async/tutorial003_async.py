import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_and_tables():
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


async def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        await session.commit()


async def select_heroes():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        statement = select(Hero)
        results = await session.exec(statement)
        heroes = results.all()
        print(heroes)


async def main():
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()


if __name__ == "__main__":
    asyncio.run(main)
