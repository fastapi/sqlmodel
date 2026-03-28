# Async Tools

SQLModel supports asynchronous execution via SQLAlchemy's `ext.asyncio`. This is very useful when working with high-concurrency applications, such as FastAPI.

## `AsyncSession` and `create_async_engine`

Instead of `create_engine`, you use `create_async_engine`. And instead of `Session`, you use `AsyncSession`.

```python
from sqlmodel import SQLModel, Field, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

# Note the +asyncpg in the database URL
async_url = "postgresql+asyncpg://user:password@localhost/db"
engine = create_async_engine(async_url, echo=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    async with AsyncSession(engine) as session:
        try:
            session.add(hero_1)
            await session.commit()
            await session.refresh(hero_1)
            print("Created hero:", hero_1)
        except Exception as e:
            await session.rollback()
            print("Failed to create hero:", e)

async def read_heroes():
    async with AsyncSession(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = await session.exec(statement)
        hero = results.first()
        print("Hero:", hero)
```

## Using with FastAPI

When integrating with FastAPI, you can use `AsyncSession` as a dependency. Note that you should explicitly handle rollbacks when performing write operations.

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import create_async_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

async_url = "postgresql+asyncpg://user:password@localhost/db"
engine = create_async_engine(async_url, echo=True)

app = FastAPI()

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/heroes/")
async def read_heroes(session: AsyncSession = Depends(get_session)):
    statement = select(Hero)
    result = await session.exec(statement)
    heroes = result.all()
    return heroes

@app.post("/heroes/")
async def create_hero(hero: Hero, session: AsyncSession = Depends(get_session)):
    try:
        session.add(hero)
        await session.commit()
        await session.refresh(hero)
        return hero
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
```
