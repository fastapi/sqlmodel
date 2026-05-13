# Async Support

SQLModel supports asynchronous operations by leveraging SQLAlchemy's `asyncio` extension.

## Setup

To use async features, you need an async database driver. For SQLite, use `aiosqlite`. For PostgreSQL, use `asyncpg`.

```bash
pip install aiosqlite
```

## Async Engine and Session

You can create an async engine using `create_async_engine` and manage sessions with `AsyncSession`.

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

DATABASE_URL = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def create_hero():
    async with AsyncSession(engine) as session:
        hero = Hero(name="Deadpond", secret_name="Dive-man")
        session.add(hero)
        await session.commit()
        await session.refresh(hero)
        print(f"Created hero: {hero.name}")

async def select_heroes():
    async with AsyncSession(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = await session.exec(statement)
        hero = results.first()
        print(f"Found hero: {hero.name}")

import asyncio

async def main():
    await init_db()
    await create_hero()
    await select_heroes()

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Differences from Sync

1. **Engine**: Use `create_async_engine` instead of `create_engine`.
2. **Session**: Use `sqlmodel.ext.asyncio.session.AsyncSession` instead of `sqlmodel.Session`.
3. **Execution**: Use `await session.exec(statement)` instead of `session.exec(statement)`.
4. **Commit/Refresh**: Use `await session.commit()` and `await session.refresh(instance)`.
5. **Table Creation**: Use `conn.run_sync(SQLModel.metadata.create_all)` because `create_all` is a synchronous method.
