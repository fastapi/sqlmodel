1. Here's a subtle thing to notice.

    Remember that [Order Matters](../create-db-and-table.md#sqlmodel-metadata-order-matters){.internal-link target=_blank} and we need to make sure all the **SQLModel** models are already defined and **imported** before calling `.create_all()`.

    IN this line, by importing something, *anything*, from `.main`, the code in `.main` will be executed, including the definition of the **table models**, and that will automatically register them in `SQLModel.metadata`.

2. Here we create a new **engine**, completely different from the one in `main.py`.

    This is the engine we will use for the tests.

    We use the new URL of the database for tests:

    ```
    sqlite:///testing.db
    ```

    And again, we use the connection argument `check_same_thread=False`.

3. Then we call:

    ```Python
    SQLModel.metadata.create_all(engine)
    ```

    ...to make sure we create all the tables in the new testing database.

    The **table models** are registered in `SQLModel.metadata` just because we imported *something* from `.main`, and the code in `.main` was executed, creating the classes for the **table models** and automatically registering them in `SQLModel.metadata`.

    So, by the point we call this method, the **table models** are already registered there. 💯

4. Here's where we create the custom **session** object for this test in a `with` block.

    It uses the new custom **engine** we created, so anything that uses this session will be using the testing database.

5. Now, back to the dependency override, it is just returning the same **session** object from outside, that's it, that's the whole trick.

6. By this point, the testing **session** `with` block finishes, and the session is closed, the file is closed, etc.
