1. We use a function `create_heroes()` to put this logic together.

2. Create each of the objects/instances of the `Hero` model.

    Each of them represents the data for one row.

3. Use a `with` block to create a `Session` using the `engine`.

    The new **sesion** will be assigned to the variable `session`.

    And it will be automatically closed when the `with` block is finished.

4. Add each of the objects/instances to the **session**.

    Each of these objects represents a row in the database.

    They are all waiting there in the session to be saved.

5. **Commit** the changes to the database.

    This will actually send the data to the database.

    It will start a transaction automatically and save all the data in a single batch.

6. By this point, after the `with` block is finished, the **session** is automatically closed.

7. We have a `main()` function with all the code that should be executed when the program is called as a **script from the console**.

    That way we can add more code later to this function.

    We then put this function `main()` in the main block below.

    And as it is a single function, other Python files could **import it** and call it directly.

8. In this `main()` function, we are also creating the database and the tables.

    In the previous version, this function was called directly in the main block.

    But now it is just called in the `main()` function.

9. And now we are also creating the heroes in this `main()` function.

10. We still have a main block to execute some code when the program is run as a script from the command line, like:

    <div class="termy">

    ```console
    $ python app.py

    // Do whatever is in the main block 🚀
    ```

    </div>

11. There's a single `main()` function now that contains all the code that should be executed when running the program from the console.

    So this is all we need to have in the main block. Just call the `main()` function.
