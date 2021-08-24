# Update Data with FastAPI

Now let's see how to update data in the database with a **FastAPI** *path operation*.

## `HeroUpdate` Model

We want clients to be able to udpate the `name`, the `secret_name`, and the `age` of a hero.

But we don't want them to have to include all the data again just to **update a single field**.

So, we need to have all those fields **marked as optional**.

And because the `HeroBase` has some of them as *required* and not optional, we will need to **create a new model**.

!!! tip
    Here is one of those cases where it probably makes sense to use an **independent model** instead of trying to come up with a complex tree of models inheriting from each other.

    Because each field is **actually different** (we just change it to `Optional`, but that's already making it different), it makes sense to have them in their own model.

So, let's create this new `HeroUpdate` model:

```Python hl_lines="21-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:7-28]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

</details>

This is almost the same as `HeroBase`, but all the fields are optional, so we can't simply inherit from `HeroBase`.

## Create the Update Path Operation

Now let's use this model in the *path operation* to update a hero.

We will use a `PATCH` HTTP operation. This is used to **partially update data**, which is what we are doing.

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

</details>

We also read the `hero_id` from the *path parameter* an the request body, a `HeroUpdate`.

### Read the Existing Hero

We take a `hero_id` with the **ID** of the hero **we want to update**.

So, we need to read the hero from the database, with the **same logic** we used to **read a single hero**, checking if it exists, possibly raising an error for the client if it doesn't exist, etc.

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

</details>

### Get the New Data

The `HeroUpdate` model has all the fields with **default values**, because they all have defaults, they are all optional, which is what we want.

But that also means that if we just call `hero.dict()` we will get a dictionary that could potentially have several or all of those values with their defaults, for example:

```Python
{
    "name": None,
    "secret_name": None,
    "age": None,
}
```

And then if we update the hero in the database with this data, we would be removing any existing values, and that's probably **not what the client intended**.

But fortunately Pydantic models (and so SQLModel models) have a parameter we can pass to the `.dict()` method for that: `exclude_unset=True`.

This tells Pydantic to **not include** the values that were **not sent** by the client. Saying it another way, it would **only** include the values that were **sent by the client**.

So, if the client sent a JSON with no values:

```JSON
{}
```

Then the dictionary we would get in Python using `hero.dict(exclude_unset=True)` would be:

```Python
{}
```

But if the client sent a JSON with:

```JSON
{
    "name": "Deadpuddle"
}
```

Then the dictionary we would get in Python using `hero.dict(exclude_unset=True)` would be:

```Python
{
    "name": "Deadpuddle"
}
```

Then we use that to get the data that was actually sent by the client:

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

</details>

## Update the Hero in the Database

Now that we have a **dictionary with the data sent by the client**, we can iterate for each one of the keys and the values, and then we set them in the database hero model `db_hero` using `setattr()`.

```Python hl_lines="10-11"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/update/tutorial001.py[ln:76-91]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/update/tutorial001.py!}
```

</details>

If you are not familiar with that `setattr()`, it takes an object, like the `db_hero`, then an attribute name (`key`), that in our case could be `"name"`, and a value (`value`). And then it **sets the attribute with that name to the value**.

So, if `key` was `"name"` and `value` was `"Deadpuddle"`, then this code:

```Python
setattr(db_hero, key, value)
```

...would be more or less equivalent to:

```Python
db_hero.name = "Deadpuddle"
```

## Remove Fields

Here's a bonus. 🎁

When getting the dictionary of data sent by the client, we only include **what the client actually sent**.

This sounds simple, but it has some additional nuances that become **nice features**. ✨

We are **not simply omitting** the data that has the **default values**.

And we are **not simply omitting** anything that is `None`.

This means that, if a model in the database **has a value different than the default**, the client could **reset it to the same value as the default**, or even `None`, and we would **still notice it** and **update it accordingly**. 🤯🚀

So, if the client wanted to intentionally remove the `age` of a hero, they could just send a JSON with:

```JSON
{
    "age": null
}
```

And when getting the data with `hero.dict(exclude_unset=True)`, we would get:

```Python
{
    "age": None
}
```

So, we would use that value and upate the `age` to `None` in the database, **just as the client intended**.

Notice that `age` here is `None`, and **we still detected it**.

Also that `name` was not even sent, and we don't *accidentaly* set it to `None` or something, we just didn't touch it, because the client didn't sent it, so we are **pefectly fine**, even in these corner cases. ✨

These are some of the advantages of Pydantic, that we can use with SQLModel. 🎉

## Recap

Using `.dict(exclude_unset=True)` in SQLModel models (and Pydantic models) we can easily update data **correctly**, even in the **edge cases**. 😎
