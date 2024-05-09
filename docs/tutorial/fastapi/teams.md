# FastAPI Path Operations for Teams - Other Models

Let's now update the **FastAPI** application to handle data for teams.

This is very similar to the things we have done for heroes, so we will go over it quickly here.

We will use the same models we used in previous examples, with the **relationship attributes**, etc.

## Add Teams Models

Let's add the models for the teams.

It's the same process we did for heroes, with a base model, a **table model**, and some other **data models**.

We have a `TeamBase` **data model**, and from it, we inherit with a `Team` **table model**.

Then we also inherit from the `TeamBase` for the `TeamCreate` and `TeamPublic` **data models**.

And we also create a `TeamUpdate` **data model**.

//// tab | Python 3.10+

```Python hl_lines="5-7  10-13  16-17  20-21  24-26"
{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:1-26]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="7-9  12-15  18-19  22-23  26-28"
{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:1-28]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7-9  12-15  18-19  22-23  26-28"
{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:1-28]!}

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

We now also have **relationship attributes**. 🎉

Let's now update the `Hero` models too.

## Update Hero Models

//// tab | Python 3.10+

```Python hl_lines="3-8  11-14  17-18  21-22  25-29"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:29-55]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-8  11-14  17-18  21-22  25-29"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:31-57]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-8  11-14  17-18  21-22  25-29"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:31-57]!}

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

We now have a `team_id` in the hero models.

Notice that we can declare the `team_id` in the `HeroBase` because it can be reused by all the models, in all the cases it's an optional integer.

And even though the `HeroBase` is *not* a **table model**, we can declare `team_id` in it with the `foreign key` parameter. It won't do anything in most of the models that inherit from `HeroBase`, but in the **table model** `Hero` it will be used to tell **SQLModel** that this is a **foreign key** to that table.

## Relationship Attributes

Notice that the **relationship attributes**, the ones with `Relationship()`, are **only** in the **table models**, as those are the ones that are handled by **SQLModel** with SQLAlchemy and that can have the automatic fetching of data from the database when we access them.

//// tab | Python 3.10+

```Python hl_lines="11  38"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:5-55]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  38"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:7-57]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  38"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:7-57]!}

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

## Path Operations for Teams

Let's now add the **path operations** for teams.

These are equivalent and very similar to the **path operations** for the **heroes** we had before, so we don't have to go over the details for each one, let's check the code.

//// tab | Python 3.10+

```Python hl_lines="3-9  12-20  23-28  31-47  50-57"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py310.py[ln:136-190]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-9  12-20  23-28  31-47  50-57"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001_py39.py[ln:138-192]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-9  12-20  23-28  31-47  50-57"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:138-192]!}

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

## Using Relationships Attributes

Up to this point, we are actually not using the **relationship attributes**, but we could access them in our code.

In the next chapter, we will play more with them.

## Check the Docs UI

Now we can check the automatic docs UI to see all the **path operations** for heroes and teams.

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/teams/image01.png">

## Recap

We can use the same patterns to add more models and API **path operations** to our **FastAPI** application. 🎉
