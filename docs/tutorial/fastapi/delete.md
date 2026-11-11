# Delete Data with FastAPI

Let's now add a *path operation* to delete a hero.

This is quite straightforward. 😁

## Delete Path Operation

Because we want to **delete** data, we use an HTTP `DELETE` operation.

We get a `hero_id` from the path parameter and verify if it exists, just as we did when reading a single hero or when updating it, **possibly raising an error** with a `404` response.

And if we actually find a hero, we just delete it with the **session**.

{* ./docs_src/tutorial/fastapi/delete/tutorial001.py ln[91:98] hl[91:98] *}

After deleting it successfully, we just return a response of:

```JSON
{
    "ok": true
}
```

## Recap

That's it, feel free to try it out in the interactive docs UI to delete some heroes. 💥

Using **FastAPI** to read data and combining it with **SQLModel** makes it quite straightforward to delete data from the database.
