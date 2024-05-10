# Update Data with FastAPI

Now let's see how to update data in the database with a **FastAPI** *path operation*.

## `HeroUpdate` Model

We want clients to be able to update the `name`, the `secret_name`, and the `age` of a hero.

But we don't want them to have to include all the data again just to **update a single field**.

So, we need to have all those fields **marked as optional**.

And because the `HeroBase` has some of them as *required* and not optional, we will need to **create a new model**.

/// tip

Here is one of those cases where it probably makes sense to use an **independent model** instead of trying to come up with a complex tree of models inheriting from each other.

Because each field is **actually different** (we just change it to `Optional`, but that's already making it different), it makes sense to have them in their own model.

///

So, let's create this new `HeroUpdate` model:

//// tab | Python 3.10+

```Python hl_lines="21-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py[ln:5-26]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="21-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py[ln:7-28]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="21-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:7-28]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

////

///

This is almost the same as `HeroBase`, but all the fields are optional, so we can't simply inherit from `HeroBase`.

## Create the Update Path Operation

Now let's use this model in the *path operation* to update a hero.

We will use a `PATCH` HTTP operation. This is used to **partially update data**, which is what we are doing.

//// tab | Python 3.10+

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py[ln:74-89]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py[ln:76-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

////

///

We also read the `hero_id` from the *path parameter* and the request body, a `HeroUpdate`.

### Read the Existing Hero

We take a `hero_id` with the **ID** of the hero **we want to update**.

So, we need to read the hero from the database, with the **same logic** we used to **read a single hero**, checking if it exists, possibly raising an error for the client if it doesn't exist, etc.

//// tab | Python 3.10+

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py[ln:74-89]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py[ln:76-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

////

///

### Get the New Data

The `HeroUpdate` model has all the fields with **default values**, because they all have defaults, they are all optional, which is what we want.

But that also means that if we just call `hero.model_dump()` we will get a dictionary that could potentially have several or all of those values with their defaults, for example:

```Python
{
    "name": None,
    "secret_name": None,
    "age": None,
}
```

And then, if we update the hero in the database with this data, we would be removing any existing values, and that's probably **not what the client intended**.

But fortunately Pydantic models (and so SQLModel models) have a parameter we can pass to the `.model_dump()` method for that: `exclude_unset=True`.

This tells Pydantic to **not include** the values that were **not sent** by the client. Saying it another way, it would **only** include the values that were **sent by the client**.

So, if the client sent a JSON with no values:

```JSON
{}
```

Then the dictionary we would get in Python using `hero.model_dump(exclude_unset=True)` would be:

```Python
{}
```

But if the client sent a JSON with:

```JSON
{
    "name": "Deadpuddle"
}
```

Then the dictionary we would get in Python using `hero.model_dump(exclude_unset=True)` would be:

```Python
{
    "name": "Deadpuddle"
}
```

Then we use that to get the data that was actually sent by the client:

//// tab | Python 3.10+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py[ln:74-89]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py[ln:76-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

////

///

/// tip
Before SQLModel 0.0.14, the method was called `hero.dict(exclude_unset=True)`, but it was renamed to `hero.model_dump(exclude_unset=True)` to be consistent with Pydantic v2.
///

## Update the Hero in the Database

Now that we have a **dictionary with the data sent by the client**, we can use the method `db_hero.sqlmodel_update()` to update the object `db_hero`.

//// tab | Python 3.10+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py[ln:74-89]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py[ln:76-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

////

///

/// tip

The method `db_hero.sqlmodel_update()` was added in SQLModel 0.0.16. 🤓

Before that, you would need to manually get the values and set them using `setattr()`.

///

The method `db_hero.sqlmodel_update()` takes an argument with another model object or a dictionary.

For each of the fields in the **original** model object (`db_hero` in this example), it checks if the field is available in the **argument** (`hero_data` in this example) and then updates it with the provided value.

## Remove Fields

Here's a bonus. 🎁

When getting the dictionary of data sent by the client, we only include **what the client actually sent**.

This sounds simple, but it has some additional nuances that become **nice features**. ✨

We are **not simply omitting** the data that has the **default values**.

And we are **not simply omitting** anything that is `None`.

This means that if a model in the database **has a value different than the default**, the client could **reset it to the same value as the default**, or even `None`, and we would **still notice it** and **update it accordingly**. 🤯🚀

So, if the client wanted to intentionally remove the `age` of a hero, they could just send a JSON with:

```JSON
{
    "age": null
}
```

And when getting the data with `hero.model_dump(exclude_unset=True)`, we would get:

```Python
{
    "age": None
}
```

So, we would use that value and update the `age` to `None` in the database, **just as the client intended**.

Notice that `age` here is `None`, and **we still detected it**.

Also, that `name` was not even sent, and we don't *accidentally* set it to `None` or something. We just didn't touch it because the client didn't send it, so we are **perfectly fine**, even in these corner cases. ✨

These are some of the advantages of Pydantic, that we can use with SQLModel. 🎉

## Recap

Using `.model_dump(exclude_unset=True)` in SQLModel models (and Pydantic models) we can easily update data **correctly**, even in the **edge cases**. 😎
