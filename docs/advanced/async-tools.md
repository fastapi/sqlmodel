# Using Asynchronous Tools with SQLModel

Before diving into the guide, it's essential to highlight a few points:

-   **FastAPI**: While FastAPI is not strictly required for using asynchronous tools with SQLModel, we'll use it in this example to simplify the demonstration.
    
-   **Database Support**: SQLite does not support asynchronous operations. To run this example, you'll need a SQL Database that supports async. Remember to change the Database URL according to your database setup. We will be using Postgres in this example.

In this guide, we'll walk through how to integrate asynchronous capabilities with SQLModel, making use of FastAPI and asyncpg with a PostgreSQL database. This will enable us to perform non-blocking database operations and benefit from better performance in web applications.

## Installation:

To run the example, you need to install some required packages. Use the following commands to do so:

```
pip install sqlmodel asyncpg fastapi uvicorn
```

## Final code
```
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel

# Initialize FastAPI application
app = FastAPI()


# Define User model for SQLModel
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int


# Define UserCreate model for Pydantic validation
# For id field to not show up on the OpenAPI spec
class UserCreate(BaseModel):
    name: str
    age: int


# Database connection string
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/sampledb"

# Create an asynchronous engine for the database
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)


# Ayschronous Context manager for handling database sessions
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


# Function to create a new user in the database
async def create_user(user: User) -> User:
    async with get_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


# Event handler for startup event of FastAPI application
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # For SQLModel, this will create the tables (but won't drop existing ones)
        await conn.run_sync(SQLModel.metadata.create_all)


# Endpoint to create a new user
@app.post("/users/", response_model=User)
async def create_user_endpoint(user: UserCreate):
    db_user = User(**user.dict())
    result = await create_user(db_user)
    return result


# Main entry point of the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


```

## Code Breakdown

### Import Necessary Libraries

```python
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel
```

Here, we're importing the required libraries and modules for our example.

### Initialize FastAPI Application

```python
app = FastAPI()
```

We create an instance of the FastAPI application.

### Define SQLModel Table

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
```

Here, we're defining a `User` model with `SQLModel`. The `table=True` argument indicates that this class should represent a database table. We define fields `id`, `name`, and `age` with appropriate types.

### Define Pydantic Model

```python
class UserCreate(BaseModel):
    name: str
    age: int
```

The `UserCreate` class serves as a data validation model using Pydantic. This ensures we only accept valid data when creating a new user.

### Database Configuration

```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/sampledb"
```

We set up the database connection string. We're using `asyncpg` with PostgreSQL for asynchronous operations.

### Create Asynchronous Engine

```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600,
)
```

We create an asynchronous engine for our database. Here, we've specified various parameters, such as `pool_size`, which determines the number of connections to maintain in the pool.

### Asynchronous Context Manager for Database Sessions

```python
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
```

We define an asynchronous context manager that provides a way to get a database session. It initializes a session, yields control to the caller for the duration of the block, and then handles cleanup once the block is exited.

### User Creation Function

```python
async def create_user(user: User) -> User:
    async with get_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
```

This function allows us to create a new user in the database. It makes use of the `get_session` context manager.

### FastAPI Startup Event

```python
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

When the FastAPI application starts, this event handler ensures that the necessary tables (in this case, the `User` table) are created if they don't already exist.

### FastAPI Endpoint to Create a New User

```python
@app.post("/users/", response_model=User)
async def create_user_endpoint(user: UserCreate):
    db_user = User(**user.dict())
    result = await create_user(db_user)
    return result
```

We define an endpoint that allows the creation of a new user. It takes in data validated against the `UserCreate` model, uses it to create a `User` object, and then stores this user in the database.

### Main Entry Point

```python
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Finally, if this script is run directly, it starts up a Uvicorn server to serve our FastAPI application on `0.0.0.0` (all available network interfaces) at port `8000`.

## Conclusion

With the combination of FastAPI, SQLModel, and asynchronous database drivers like asyncpg, we can create highly performant web applications that handle database interactions efficiently. This example demonstrates the essentials of setting up asynchronous operations with SQLModel in the context of a FastAPI application.