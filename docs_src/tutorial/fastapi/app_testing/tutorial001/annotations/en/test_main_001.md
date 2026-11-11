1. Import the `app` from the the `main` module.

2. We create a `TestClient` for the FastAPI `app` and put it in the variable `client`.

3. Then we use use this `client` to **talk to the API** and send a `POST` HTTP operation, creating a new hero.

4. Then we get the **JSON data** from the response and put it in the variable `data`.

5. Next we start testing the results with `assert` statements, we check that the status code of the response is `200`.

6. We check that the `name` of the hero created is `"Deadpond"`.

7. We check that the `secret_name` of the hero created is `"Dive Wilson"`.

8. We check that the `age` of the hero created is `None`, because we didn't send an age.

9. We check that the hero created has an `id` created by the database, so it's not `None`.
