1. Import `pytest`.

2. Use the `@pytest.fixture()` decorator on top of the function to tell pytest that this is a **fixture** function (equivalent to a FastAPI dependency).

    We also give it a name of `"session"`, this will be important in the testing function.

3. Create the fixture function. This is equivalent to a FastAPI dependency function.

    In this fixture we create the custom **engine**, with the in-memory database, we create the tables, and we create the **session**.

    Then we `yield` the `session` object.

4. The thing that we `return` or `yield` is what will be available to the test function, in this case, the `session` object.

    Here we use `yield` so that **pytest** comes back to execute "the rest of the code" in this function once the testing function is done.

    We don't have any more visible "rest of the code" after the `yield`, but we have the end of the `with` block that will close the **session**.

    By using `yield`, pytest will:

    * run the first part
    * create the **session** object
    * give it to the test function
    * run the test function
    * once the test function is done, it will continue here, right after the `yield`, and will correctly close the **session** object in the end of the `with` block.

5. Now, in the test function, to tell **pytest** that this test wants to get the fixture, instead of declaring something like in FastAPI with:

    ```Python
    session: Session = Depends(session_fixture)
    ```

    ...the way we tell pytest what is the fixture that we want is by using the **exact same name** of the fixture.

    In this case, we named it `session`, so the parameter has to be exactly named `session` for it to work.

    We also add the type annotation `session: Session` so that we can get autocompletion and inline error checks in our editor.

6. Now in the dependency override function, we just return the same `session` object that came from outside it.

    The `session` object comes from the parameter passed to the test function, and we just re-use it and return it here in the dependency override.
