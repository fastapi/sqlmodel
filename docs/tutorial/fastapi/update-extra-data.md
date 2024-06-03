# Update with Extra Data (Hashed Passwords) with FastAPI

In the previous chapter I explained to you how to update data in the database from input data coming from a **FastAPI** *path operation*.

Now I'll explain to you how to add **extra data**, additional to the input data, when updating or creating a model object.

This is particularly useful when you need to **generate some data** in your code that is **not coming from the client**, but you need to store it in the database. For example, to store a **hashed password**.

## Password Hashing

Let's imagine that each hero in our system also has a **password**.

We should never store the password in plain text in the database, we should only stored a **hashed version** of it.

"**Hashing**" means converting some content (a password in this case) into a sequence of bytes (just a string) that looks like gibberish.

Whenever you pass exactly the same content (exactly the same password) you get exactly the same gibberish.

But you **cannot convert** from the gibberish **back to the password**.

### Why use Password Hashing

If your database is stolen, the thief won't have your users' **plaintext passwords**, only the hashes.

So, the thief won't be able to try to use that password in another system (as many users use the same password everywhere, this would be dangerous).

/// tip

You could use <a href="https://passlib.readthedocs.io/en/stable/" class="external-link" target="_blank">passlib</a> to hash passwords.

In this example we will use a fake hashing function to focus on the data changes. 🤡

///

## Update Models with Extra Data

The `Hero` table model will now store a new field `hashed_password`.

And the data models for `HeroCreate` and `HeroUpdate` will also have a new field `password` that will contain the plain text password sent by clients.

//// tab | Python 3.10+

```Python hl_lines="11  15  26"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:5-28]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  15  26"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:7-30]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  15  26"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:7-30]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002.py!}
```

////

///

When a client is creating a new hero, they will send the `password` in the request body.

And when they are updating a hero, they could also send the `password` in the request body to update it.

## Hash the Password

The app will receive the data from the client using the `HeroCreate` model.

This contains the `password` field with the plain text password, and we cannot use that one. So we need to generate a hash from it.

//// tab | Python 3.10+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:55-57]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:44-46]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:57-59]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:44-46]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:57-59]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002.py!}
```

////

///

## Create an Object with Extra Data

Now we need to create the database hero.

In previous examples, we have used something like:

```Python
db_hero = Hero.model_validate(hero)
```

This creates a `Hero` (which is a *table model*) object from the `HeroCreate` (which is a *data model*) object that we received in the request.

And this is all good... but as `Hero` doesn't have a field `password`, it won't be extracted from the object `HeroCreate` that has it.

`Hero` actually has a `hashed_password`, but we are not providing it. We need a way to provide it...

### Dictionary Update

Let's pause for a second to check this, when working with dictionaries, there's a way to `update` a dictionary with extra data from another dictionary, something like this:

```Python hl_lines="14"
db_user_dict = {
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": None,
}

hashed_password = "fakehashedpassword"

extra_data = {
    "hashed_password": hashed_password,
    "age": 32,
}

db_user_dict.update(extra_data)

print(db_user_dict)

# {
#     "name": "Deadpond",
#     "secret_name": "Dive Wilson",
#     "age": 32,
#     "hashed_password": "fakehashedpassword",
# }
```

This `update` method allows us to add and override things in the original dictionary with the data from another dictionary.

So now, `db_user_dict` has the updated `age` field with `32` instead of `None` and more importantly, **it has the new `hashed_password` field**.

### Create a Model Object with Extra Data

Similar to how dictionaries have an `update` method, **SQLModel** models have a parameter `update` in `Hero.model_validate()` that takes a dictionary with extra data, or data that should take precedence:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:55-64]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:57-66]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:57-66]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002.py!}
```

////

///

Now, `db_hero` (which is a *table model* `Hero`) will extract its values from `hero` (which is a *data model* `HeroCreate`), and then it will **`update`** its values with the extra data from the dictionary `extra_data`.

It will only take the fields defined in `Hero`, so **it will not take the `password`** from `HeroCreate`. And it will also **take its values** from the **dictionary passed to the `update`** parameter, in this case, the `hashed_password`.

If there's a field in both `hero` and the `extra_data`, **the value from the `extra_data` passed to `update` will take precedence**.

## Update with Extra Data

Now let's say we want to **update a hero** that already exists in the database.

The same way as before, to avoid removing existing data, we will use `exclude_unset=True` when calling `hero.model_dump()`, to get a dictionary with only the data sent by the client.

//// tab | Python 3.10+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:83-89]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:85-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:85-91]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002.py!}
```

////

///

Now, this `hero_data` dictionary could contain a `password`. We need to check it, and if it's there, we need to generate the `hashed_password`.

Then we can put that `hashed_password` in a dictionary.

And then we can update the `db_hero` object using the method `db_hero.sqlmodel_update()`.

It takes a model object or dictionary with the data to update the object and also an **additional `update` argument** with extra data.

//// tab | Python 3.10+

```Python hl_lines="15"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py[ln:83-99]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="15"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py[ln:85-101]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="15"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial002.py[ln:85-101]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/update/tutorial002.py!}
```

////

///

/// tip

The method `db_hero.sqlmodel_update()` was added in SQLModel 0.0.16. 😎

///

## Recap

You can use the `update` parameter in `Hero.model_validate()` to provide extra data when creating a new object and `Hero.sqlmodel_update()` to provide extra data when updating an existing object. 🤓
