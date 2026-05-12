# Async Database Sessions

SQLModel supports asynchronous database sessions using SQLAlchemy's async features. This is particularly useful when building asynchronous applications with frameworks like **FastAPI**.

## Create the Async Engine

To use async sessions, you need to use an async database driver (like `aiosqlite` for SQLite or `asyncpg` for PostgreSQL) and create an async engine using `create_async_engine`.

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

sqlite_url = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(sqlite_url, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

## Async Session

Instead of the standard `Session`, you use `AsyncSession` from `sqlalchemy.ext.asyncio`.

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
```

## Async CRUD Operations

When using `AsyncSession`, you must `await` operations that communicate with the database.

### Create

```python
async def create_hero(session: AsyncSession):
    hero = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero
```

### Read

For queries, use `session.exec()` (or `session.execute()`) and `await` the result.

```python
from sqlmodel import select

async def read_heroes(session: AsyncSession):
    statement = select(Hero)
    results = await session.exec(statement)
    heroes = results.all()
    return heroes
```

### Update and Delete

Update and delete operations also require `awaiting` the commit.

```python
async def update_hero(session: AsyncSession, hero_id: int, new_name: str):
    hero = await session.get(Hero, hero_id)
    if hero:
        hero.name = new_name
        session.add(hero)
        await session.commit()
        await session.refresh(hero)
    return hero

async def delete_hero(session: AsyncSession, hero_id: int):
    hero = await session.get(Hero, hero_id)
    if hero:
        await session.delete(hero)
        await session.commit()
```

---

Payment Address (SOL/RTC): `BVf9eNCQFSamVQ2VwkQZ9UvkUX37j7Syk75DvZtutJef`
