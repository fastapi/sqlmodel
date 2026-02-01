# Async SQLModel

SQLModel supports asynchronous database operations out of the box using SQLAlchemy's async features and the `AsyncSession` provided by SQLModel.

## When to use Async

Asynchronous programming is particularly useful for Web APIs (like FastAPI) that handle many concurrent connections and spend much of their time waiting for the database to respond.

## Create the Async Engine

To use async, you need an async database driver (like `aiosqlite` for SQLite or `asyncpg` for PostgreSQL).

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

sqlite_url = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(sqlite_url, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

## Use AsyncSession

Use `from sqlmodel.ext.asyncio.session import AsyncSession` to perform async operations.

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

async def get_heroes():
    async with AsyncSession(engine) as session:
        statement = select(Hero)
        results = await session.exec(statement)
        return results.all()
```

## Integration with FastAPI

In FastAPI, you can use a dependency to provide an `AsyncSession`:

```python
async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```
