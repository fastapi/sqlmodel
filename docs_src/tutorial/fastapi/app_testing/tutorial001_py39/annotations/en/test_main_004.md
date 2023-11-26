1. Import `StaticPool` from `sqlmodel`, we will use it in a bit.

2. For the **SQLite URL**, don't write any file name, leave it empty.

    So, instead of:

    ```
    sqlite:///testing.db
    ```

    ...just write:

    ```
    sqlite://
    ```

    This is enough to tell **SQLModel** (actually SQLAlchemy) that we want to use an **in-memory SQLite database**.

3. Remember that we told the **low-level** library in charge of communicating with SQLite that we want to be able to **access the database from different threads** with `check_same_thread=False`?

    Now that we use an **in-memory database**, we need to also tell SQLAlchemy that we want to be able to use the **same in-memory database** object from different threads.

    We tell it that with the `poolclass=StaticPool` parameter.

    !!! info
        You can read more details in the <a href="https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#using-a-memory-database-in-multiple-threads" class="external-link" target="_blank">SQLAlchemy documentation about Using a Memory Database in Multiple Threads</a>
