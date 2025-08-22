1. Create the new fixture named `"client"`.

2. This **client fixture**, in turn, also requires the **session fixture**.

3. Now we create the **dependency override** inside the client fixture.

4. Set the **dependency override** in the `app.dependency_overrides` dictionary.

5. Create the `TestClient` with the **FastAPI** `app`.

6. `yield` the `TestClient` instance.

    By using `yield`, after the test function is done, pytest will come back to execute the rest of the code after `yield`.

7. This is the cleanup code, after `yield`, and after the test function is done.

    Here we clear the dependency overrides (here it's only one) in the FastAPI `app`.

8. Now the test function requires the **client fixture**.

    And inside the test function, the code is quite **simple**, we just use the `TestClient` to make requests to the API, check the data, and that's it.

    The fixtures take care of all the **setup** and **cleanup** code.
