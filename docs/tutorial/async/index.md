# Async with SQLModel

**SQLModel** is based on SQLAlchemy, which has great support for `async` and `await` with `asyncio`.

You can use **SQLModel** in an asynchronous way as well.

## Install `aiosqlite`

For this example, we will use **SQLite** with the `aiosqlite` driver to make it asynchronous.

Make sure you install `aiosqlite`:

<div class="termy">

```console
$ pip install aiosqlite
---> 100%
```

</div>

## Create the Async Engine

Instead of `create_engine`, we use `create_async_engine` from `sqlalchemy.ext.asyncio`.

And we change the connection URL to use `sqlite+aiosqlite`.

{* ./docs_src/tutorial/async/tutorial001_py310.py ln[1:16] hl[2,15:16] *}

## Async Session

To use an asynchronous session, we use `AsyncSession` from `sqlmodel.ext.asyncio`.

It is a subclass of SQLAlchemy's `AsyncSession` with added support for SQLModel's `exec()` method.

## Create the Database and Tables

When using an async engine, we cannot call `SQLModel.metadata.create_all(engine)` directly because it is a synchronous operation.

Instead, we use `engine.begin()` and `conn.run_sync()`.

{* ./docs_src/tutorial/async/tutorial001_py310.py ln[19:21] hl[19:21] *}

## Async FastAPI Dependency

We can create an async dependency to get the session.

{* ./docs_src/tutorial/async/tutorial001_py310.py ln[27:30] hl[27:30] *}

## Async Path Operations

Now we can use `async def` for our path operations and `await` the session methods.

We use `await session.exec()` to execute queries, and `await session.commit()`, `await session.refresh()` for mutations.

{* ./docs_src/tutorial/async/tutorial001_py310.py ln[33:45] hl[35:37,42:43] *}

## Full Example

Here is the complete file:

{* ./docs_src/tutorial/async/tutorial001_py310.py *}

## Common Pitfalls and Best Practices

### Use `await` for Database Operations

When using `AsyncSession`, remember to `await` all methods that interact with the database.

This includes:
* `session.exec()`
* `session.commit()`
* `session.refresh()`
* `session.get()`
* `session.delete()`

### Relationships and Lazy Loading

By default, SQLAlchemy (and SQLModel) uses "lazy loading" for relationships. In synchronous code, this means that when you access a relationship attribute, it automatically fetches the data from the database.

In asynchronous code, **lazy loading is not supported** because it would need to perform I/O without an `await`.

If you try to access a relationship that hasn't been loaded yet, you will get an error.

To solve this, you should use **eager loading** with `selectinload`.

```Python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

# ...

async def read_heroes(session: AsyncSession):
    statement = select(Hero).options(selectinload(Hero.team))
    result = await session.exec(statement)
    heroes = result.all()
    return heroes
```

### Async Database Drivers

Make sure you use an asynchronous database driver. 

* For **SQLite**, use `aiosqlite` with `sqlite+aiosqlite://`.
* For **PostgreSQL**, use `asyncpg` with `postgresql+asyncpg://`.

If you use a synchronous driver (like `sqlite://` or `postgresql://`), it will not work with `create_async_engine`.
