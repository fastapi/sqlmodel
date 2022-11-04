import asyncio
from typing import Annotated, Optional

# TODO change when https://github.com/tiangolo/sqlmodel/pull/435 accepted
# TODO replace following 3 lines with:
# ------ from sqlmodel import AsyncSession, create_async_engine, Field, SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


class Team(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(index=True)]
    headquarters: str


class Hero(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(index=True)]
    secret_name: str
    age: Annotated[Optional[int], Field(default_factory=lambda: None, index=True)]

    team_id: Annotated[
        Optional[int], Field(default_factory=lambda: None, foreign_key="team.id")
    ]


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_and_tables() -> None:
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


async def create_heroes() -> None:

    async with AsyncSession(engine, expire_on_commit=False) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        await session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        await session.commit()

        await session.refresh(hero_deadpond)
        await session.refresh(hero_rusty_man)
        await session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


async def select_heroes() -> None:
    async with AsyncSession(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = await session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)


async def main() -> None:
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()


if __name__ == "__main__":
    asyncio.run(main())
