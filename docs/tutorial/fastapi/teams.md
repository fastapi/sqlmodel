# FastAPI Path Opeartions for Teams - Other Models

Let's now update the **FastAPI** application to handle data for teams.

This is very similar to the things we have done for heroes, so we will go over it quickly here.

We will use the same models we used in previous examples, with the **relationship attributes**, etc.

## Add Teams Models

Let's add the models for the teams.

It's the same process we did for heroes, with a base model, a **table model**, and some other **data models**.

We have a `TeamBase` **data model**, and from it we inherit with a `Team` **table model**.

Then we also inherit from the `TeamBase` for the `TeamCreate` and `TeamRead` **data models**.

And we also create a `TeamUpdate` **data model**.

```Python hl_lines="7-9  12-15  18-19  22-23  26-29"
{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:1-29]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

</details>

We now also have **relationship attributes**. 🎉

Let's now update the `Hero` models too.

## Update Hero Models

```Python hl_lines="3-8  11-15  17-18  21-22  25-29"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:32-58]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

</details>

We now have a `team_id` in the hero models.

Notice that we can declare the `team_id` in the `HeroBase` because it can be reused by all the models, in all the cases it's an optional integer.

And even though the `HeroBase` is *not* a **table model**, we can declare `team_id` in it with the `foreign key` parameter. It won't do anything in most of the models that inherit from `HeroBase`, but in the **table model** `Hero` it will be used to tell **SQLModel** that this is a **foreign key** to that table.

## Relationship Attributes

Notice that the **relationship attributes**, the ones with `Relationship()`, are **only** in the **table models**, as those are the ones that are handled by **SQLModel** with SQLAlchemy and that can have the automatic fetching of data from the database when we access them.

```Python hl_lines="11  39"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:7-58]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

</details>

## Path Operations for Teams

Let's now add the **path operations** for teams.

These are equivalent and very similar to the **path operations** for the **heroes** we had before, so we don't have to go over the details for each one, let's check the code.

```Python hl_lines="3-9  12-20  23-28  31-47  50-57"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/teams/tutorial001.py[ln:140-194]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/teams/tutorial001.py!}
```

</details>

## Using Relationships Attributes

Up to this point we are actually not using the **relationship attributes**, but we could access them in our code.

In the next chapter we will play more with them.

## Check the Docs UI

Now we can check the automatic docs UI to see all the **path operations** for heroes and teams.

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/teams/image01.png">

## Recap

We can use the same patterns to add more models and API **path operations** to our **FastAPI** application. 🎉
