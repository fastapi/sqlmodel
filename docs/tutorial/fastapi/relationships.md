# Models with Relationships in FastAPI

If we go right now and read a single **hero** by ID, we get the hero data with the team ID.

But we don't get any data about the particular team:

<img class="shadow" alt="Interactive API docs UI getting a single hero" src="/img/tutorial/fastapi/relationships/image01.png">

We get a response of:

```JSON hl_lines="5"
{
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": null,
    "team_id": 1,
    "id": 1,
}
```

And the same way, if we get a **team** by ID, we get the team data, but we don't get any information about this team's heroes:

<img class="shadow" alt="Interactive API docs UI getting a single team" src="/img/tutorial/fastapi/relationships/image02.png">

Here we get a response of:

```JSON
{
    "name": "Preventers",
    "headquarters": "Sharp Tower",
    "id": 2
}
```

...but no information about the heroes.

Let's update that. 🤓

## Why Aren't We Getting More Data

First, why is it that we are not getting the related data for each hero and for each team?

It's because we declared the `HeroPublic` with only the same base fields of the `HeroBase` plus the `id`. But it doesn't include a field `team` for the **relationship attribute**.

And the same way, we declared the `TeamPublic` with only the same base fields of the `TeamBase` plus the `id`. But it doesn't include a field `heroes` for the **relationship attribute**.

//// tab | Python 3.10+

```Python hl_lines="3-5  9-10  14-19  23-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:5-7]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:20-21]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:29-34]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:43-44]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-5  9-10  14-19  23-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:7-9]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:22-23]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:31-36]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:45-46]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-5  9-10  14-19  23-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:7-9]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:22-23]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:31-36]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:45-46]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

////

///

Now, remember that <a href="https://fastapi.tiangolo.com/tutorial/response-model/" class="external-link" target="_blank">FastAPI uses the `response_model` to validate and **filter** the response data</a>?

In this case, we used `response_model=TeamPublic` and `response_model=HeroPublic`, so FastAPI will use them to filter the response data, even if we return a **table model** that includes **relationship attributes**:

//// tab | Python 3.10+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:102-107]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:156-161]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:104-109]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:158-163]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:104-109]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:158-163]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

////

///

## Don't Include All the Data

Now let's stop for a second and think about it.

We cannot simply include *all* the data, including all the internal relationships, because each **hero** has an attribute `team` with their team, and then that **team** also has an attribute `heroes` with all the **heroes** in the team, including this one.

If we tried to include everything, we could make the server application **crash** trying to extract **infinite data**, going through the same hero and team over and over again internally, something like this:

```JSON hl_lines="2  13  24  34"
{
    "name": "Rusty-Man",
    "secret_name": "Tommy Sharp",
    "age": 48,
    "team_id": 1,
    "id": 1,
    "team": {
        "name": "Preventers",
        "headquarters": "Sharp Tower",
        "id": 2,
        "heroes": [
            {
                "name": "Rusty-Man",
                "secret_name": "Tommy Sharp",
                "age": 48,
                "team_id": 1,
                "id": 1,
                "team": {
                    "name": "Preventers",
                    "headquarters": "Sharp Tower",
                    "id": 2,
                    "heroes": [
                        {
                            "name": "Rusty-Man",
                            "secret_name": "Tommy Sharp",
                            "age": 48,
                            "team_id": 1,
                            "id": 1,
                            "team": {
                                "name": "Preventers",
                                "headquarters": "Sharp Tower",
                                "id": 2,
                                "heroes": [
                                    ...with infinite data here... 😱
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
}
```

As you can see, in this example, we would get the hero **Rusty-Man**, and from this hero we would get the team **Preventers**, and then from this team we would get its heroes, of course, including **Rusty-Man**... 😱

So we start again, and in the end, the server would just crash trying to get all the data with a `"Maximum recursion error"`, we would not even get a response like the one above.

So, we need to carefully choose in which cases we want to include data and in which not.

## What Data to Include

This is a decision that will depend on **each application**.

In our case, let's say that if we get a **list of heroes**, we don't want to also include each of their teams in each one.

And if we get a **list of teams**, we don't want to get a list of the heroes for each one.

But if we get a **single hero**, we want to include the team data (without the team's heroes).

And if we get a **single team**, we want to include the list of heroes (without each hero's team).

Let's add a couple more **data models** that declare that data so we can use them in those two specific *path operations*.

## Models with Relationships

Let's add the models `HeroPublicWithTeam` and `TeamPublicWithHeroes`.

We'll add them **after** the other models so that we can easily reference the previous models.

//// tab | Python 3.10+

```Python hl_lines="3-4  7-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py310.py[ln:59-64]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-4  7-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py39.py[ln:61-66]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-4  7-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001.py[ln:61-66]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001.py!}
```

////

///

These two models are very **simple in code**, but there's a lot happening here. Let's check it out.

### Inheritance and Type Annotations

The `HeroPublicWithTeam` **inherits** from `HeroPublic`, which means that it will have the **normal fields for reading**, including the required `id` that was declared in `HeroPublic`.

And then it adds the **new field** `team`, which could be `None`, and is declared with the type `TeamPublic` with the base fields for reading a team.

Then we do the same for the `TeamPublicWithHeroes`, it **inherits** from `TeamPublic`, and declares the **new field** `heroes`, which is a list of `HeroPublic`.

### Data Models Without Relationship Attributes

Now, notice that these new fields `team` and `heroes` are not declared with `Relationship()`, because these are not **table models**, they cannot have **relationship attributes** with the magic access to get that data from the database.

Instead, here these are only **data models** that will tell FastAPI **which attributes** to get data from and **which data** to get from them.

### Reference to Other Models

Also, notice that the field `team` is not declared with this new `TeamPublicWithHeroes`, because that would again create that infinite recursion of data. Instead, we declare it with the normal `TeamPublic` model.

And the same for `TeamPublicWithHeroes`, the model used for the new field `heroes` uses `HeroPublic` to get only each hero's data.

This also means that, even though we have these two new models, **we still need the previous ones**, `HeroPublic` and `TeamPublic`, because we need to reference them here (and we are also using them in the rest of the *path operations*).

## Update the Path Operations

Now we can update the *path operations* to use the new models.

This will tell **FastAPI** to take the object that we return from the *path operation function* (a **table model**) and **access the additional attributes** from them to extract their data.

In the case of the hero, this tells FastAPI to extract the `team` too. And in the case of the team, to extract the list of `heroes` too.

//// tab | Python 3.10+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py310.py[ln:111-116]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py310.py[ln:165-170]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py39.py[ln:113-118]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/relationships/tutorial001_py39.py[ln:167-172]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  8  12  17"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/relationships/tutorial001.py[ln:113-118]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/relationships/tutorial001.py[ln:167-172]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/relationships/tutorial001.py!}
```

////

///

## Check It Out in the Docs UI

Now let's try it out again in the **docs UI**.

Let's try again with the same **hero** with ID `1`:

<img class="shadow" alt="Interactive API docs UI getting a single hero with team" src="/img/tutorial/fastapi/relationships/image03.png">

Now we get the **team** data included:

```JSON hl_lines="7-11"
{
    "name": "Deadpond",
    "secret_name": "Dive Wilson",
    "age": null,
    "team_id": 1,
    "id": 1,
    "team": {
        "name": "Z-Force",
        "headquarters": "Sister Margaret's Bar",
        "id": 1
    }
}
```

And if we get now the **team** with ID `2`:

<img class="shadow" alt="Interactive API docs UI getting a single team with the list of heroes" src="/img/tutorial/fastapi/relationships/image04.png">

Now we get the list of **heroes** included:

```JSON hl_lines="5-41"
{
    "name": "Preventers",
    "headquarters": "Sharp Tower",
    "id": 2,
    "heroes": [
        {
            "name": "Rusty-Man",
            "secret_name": "Tommy Sharp",
            "age": 48,
            "team_id": 2,
            "id": 2
        },
        {
            "name": "Spider-Boy",
            "secret_name": "Pedro Parqueador",
            "age": null,
            "team_id": 2,
            "id": 3
        },
        {
            "name": "Tarantula",
            "secret_name": "Natalia Roman-on",
            "age": 32,
            "team_id": 2,
            "id": 6
        },
        {
            "name": "Dr. Weird",
            "secret_name": "Steve Weird",
            "age": 36,
            "team_id": 2,
            "id": 7
        },
        {
            "name": "Captain North America",
            "secret_name": "Esteban Rogelios",
            "age": 93,
            "team_id": 2,
            "id": 8
        }
    ]
}
```

## Recap

Using the same techniques to declare additional **data models**, we can tell FastAPI what data to return in the responses, even when we return **table models**.

Here we almost **didn't have to change the FastAPI app** code, but of course, there will be cases where you need to get the data and process it in different ways in the *path operation function* before returning it.

But even in those cases, you will be able to define the **data models** to use in `response_model` to tell FastAPI how to validate and filter the data.

By this point, you already have a very robust API to handle data in a SQL database combining **SQLModel** with **FastAPI**, and implementing **best practices**, like data validation, conversion, filtering, and documentation. ✨

In the next chapter, I'll tell you how to implement automated **testing** for your application using FastAPI and SQLModel. ✅
