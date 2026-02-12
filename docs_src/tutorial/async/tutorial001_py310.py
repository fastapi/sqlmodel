from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio import AsyncSession


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@app.post("/heroes/", response_model=Hero)
async def create_hero(hero: Hero, session: AsyncSession = Depends(get_session)):
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero


@app.get("/heroes/", response_model=list[Hero])
async def read_heroes(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Hero))
    heroes = result.all()
    return heroes
