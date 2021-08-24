1. Import `Optional` from `typing` to declare fields that could be `None`.
2. Import the things we will need from `sqlmodel`: `Field`, `SQLModel`, `create_engine`.
3. Create the `Hero` model class, representing the `hero` table in the database.

    And also mark this class as a **table model** with `table=True`.

4. Create the `id` field:

    It could be `None` until the database assigns a value to it, so we annotate it with `Optional`.

    It is a **primary key**, so we use `Field()` and the argument `primary_key=True`.

5. Create the `name` field.

    It is required, so there's no default value, and it's not `Optional`.

6. Create the `secret_name` field.

    Also required.

7. Create the `age` field.

    It is not required, the default value is `None`.

    In the database, the default value will be `NULL`, the SQL equivalent of `None`.

    As this field could be `None` (and `NULL` in the database), we annotate it with `Optional`.

8. Write the name of the database file.
9. Use the name of the database file to create the database URL.
10. Create the engine using the URL.

    This doesn't create the database yet, no file or table is created at this point, only the **engine** object that will handle the connections with this specific database, and with specific support for SQLite (based on the URL).

11. Put the code that creates side effects in a function.

    In this case, only one line that creates the database file with the table.

12. Create all the tables that were automatically registered in `SQLModel.metadata`.

13. Add a main block, or "Top-level script environment".

    And put some logic to be executed when this is called directly with Python, as in:

    <div class="termy">

    ```console
    $ python app.py

    // Execute all the stuff and show the output
    ```

    </div>

    ...but that is not executed when importing something from this module, like:

    ```Python
    from app import Hero
    ```

14. In this main block, call the function that creates the database file and the table.

    This way when we call it with:

    <div class="termy">

    ```console
    $ python app.py

    // Doing stuff ✨
    ```

    </div>

    ...it will create the database file and the table.
