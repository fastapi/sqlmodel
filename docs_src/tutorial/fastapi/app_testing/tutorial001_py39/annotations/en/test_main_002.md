1. Import the `get_session` dependency from the the `main` module.

2. Define the new function that will be the new **dependency override**.

3. This function will return a different **session** than the one that would be returned by the original `get_session` function.

    We haven't seen how this new **session** object is created yet, but the point is that this is a different session than the original one from the app.

    This session is attached to a different **engine**, and that different **engine** uses a different URL, for a database just for testing.

    We haven't defined that new **URL** nor the new **engine** yet, but here we already see the that this object `session` will override the one returned by the original dependency  `get_session()`.

4. Then, the FastAPI `app` object has an attribute `app.dependency_overrides`.

    This attribute is a dictionary, and we can put dependency overrides in it by passing, as the **key**, the **original dependency function**, and as the **value**, the **new overriding dependency function**.

    So, here we are telling the FastAPI app to use `get_session_override` instead of `get_session` in all the places in the code that depend on `get_session`, that is, all the parameters with something like:

    ```Python
    session: Session = Depends(get_session)
    ```

5. After we are done with the dependency override, we can restore the application back to normal, by removing all the values in this dictionary `app.dependency_overrides`.

    This way whenever a *path operation function* needs the dependency FastAPI will use the original one instead of the override.
