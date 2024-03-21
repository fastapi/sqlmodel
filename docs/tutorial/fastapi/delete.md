# Delete Data with FastAPI

Let's now add a *path operation* to delete a hero.

This is quite straightforward. 😁

## Delete Path Operation

Because we want to **delete** data, we use an HTTP `DELETE` operation.

We get a `hero_id` from the path parameter and verify if it exists, just as we did when reading a single hero or when updating it, **possibly raising an error** with a `404` response.

And if we actually find a hero, we just delete it with the **session**.

//// tab | Python 3.10+

```Python hl_lines="3-11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001_py310.py[ln:89-97]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001_py39.py[ln:91-99]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001.py[ln:91-99]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001.py!}
```

////

///

After deleting it successfully, we just return a response of:

```JSON
{
    "ok": true
}
```

## Recap

That's it, feel free to try it out in the interactive docs UI to delete some heroes. 💥

Using **FastAPI** to read data and combining it with **SQLModel** makes it quite straightforward to delete data from the database.
