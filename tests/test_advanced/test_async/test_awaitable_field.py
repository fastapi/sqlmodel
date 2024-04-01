from typing import Awaitable, List, Optional

import pytest
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.util.concurrency import greenlet_spawn
from sqlmodel import Field, Relationship, SQLModel, select
from sqlmodel.ext.asyncio.async_model import AsyncSQLModel, AwaitableField
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_awaitable_nomral_field(clear_sqlmodel):
    class Hero(AsyncSQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None
        awt_name: Awaitable[str] = AwaitableField(field="name")
        awt_age: Awaitable[str] = AwaitableField(field="age")

    hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson")

    engine = create_async_engine("sqlite+aiosqlite://")
    await greenlet_spawn(SQLModel.metadata.create_all, engine.sync_engine)

    async with AsyncSession(engine) as session:
        session.add(hero_deadpond)
        await session.commit()

        # loading expired attribute will raise MissingGreenlet error
        with pytest.raises(MissingGreenlet):
            hero_deadpond.name  # noqa: B018

        name = await hero_deadpond.awt_name
        assert name == "Deadpond"


@pytest.mark.asyncio
async def test_awaitable_relation_field(clear_sqlmodel):
    class Team(AsyncSQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str = Field(index=True)

        heroes: List["Hero"] = Relationship()
        awt_heroes: Awaitable[List["Hero"]] = AwaitableField(field="heroes")

    class Hero(AsyncSQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str

        team_id: Optional[int] = Field(default=None, foreign_key="team.id")
        team: Optional[Team] = Relationship(back_populates="heroes")
        awt_team: Awaitable[Optional[Team]] = AwaitableField(field="team")

    team_preventers = Team(name="Preventers")
    hero_rusty_man = Hero(name="Rusty-Man", team=team_preventers)

    engine = create_async_engine("sqlite+aiosqlite://")
    await greenlet_spawn(SQLModel.metadata.create_all, engine.sync_engine)

    async with AsyncSession(engine) as session:
        session.add(hero_rusty_man)
        await session.commit()

    async with AsyncSession(engine) as session:
        hero = (await session.exec(select(Hero).where(Hero.name == "Rusty-Man"))).one()

        # loading lazy loading attribute will raise MissingGreenlet error
        with pytest.raises(MissingGreenlet):
            hero.team  # noqa: B018

        team = await hero.awt_team
        assert team
        assert team.name == "Preventers"
