# Create Models with a Many-to-Many Link

We'll now support **many-to-many** relationships using a **link table** like this:

<img alt="many-to-many table relationships" src="/img/tutorial/many-to-many/many-to-many.svg">

Let's start by defining the class models, including the **link table** model.

## Link Table Model

As we want to support a **many-to-many** relationship, now we need a **link table** to connect them.

We can create it just as any other **SQLModel**:

```Python hl_lines="6-12"
{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:1-12]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

</details>

This is a **SQLModel** class model table like any other.

It has two fields, `team_id` and `hero_id`.

They are both **foreign keys** to their respective tables. We'll create those models in a second, but you already know how that works.

And **both fields are primary keys**. We hadn't used this before. 🤓

## Team Model

Let's see the `Team` model, it's almost identical as before, but with a little change:

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:15-20]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

</details>

The **relationship attribute `heroes`** is still a list of heroes, annotated as `List["Hero"]`. Again, we use `"Hero"` in quotes because we haven't declared that class yet by this point in the code (but as you know, editors and **SQLModel** understand that).

We use the same **`Relationship()`** function.

We use **`back_populates="teams"`**. Before we referenced an attribute `team`, but as now we can have many, we'll rename it to `teams` when creating the `Hero` model.

And here's the important part to allow the **many-to-many** relationship, we use **`link_model=HeroTeamLink`**. That's it. ✨

## Hero Model

Let's see the other side, here's the `Hero` model:

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:23-29]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

</details>

We **removed** the previous `team_id` field (column) because now the relationship is done via the link table. 🔥

The relationship attribute is now named **`teams`** instead of `team`, as now we support multiple teams.

It is no longer an `Optional[Team]` but a list of teams, annotated as **`List[Team]`**.

We are using the **`Relationship()`** here too.

We still have **`back_populates="heroes"`** as before.

And now we have a **`link_model=HeroTeamLink`**. ✨

## Create the Tables

The same as before, we will have the rest of the code to create the **engine**, and a function to create all the tables `create_db_and_tables()`.

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:32-39]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

</details>


And as in previous examples, we will add that function to a function `main()`, and we will call that `main()` function in the main block:

```Python hl_lines="4"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:78-79]!}
    # We will do more stuff here later 👈

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:83-84]!}
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

</details>


## Run the Code

If you run the code in the command line, it would output:

<div class="termy">

```console
$ python app.py

// Boilerplate omitted 😉

INFO Engine 
CREATE TABLE team (
        id INTEGER, 
        name VARCHAR NOT NULL, 
        headquarters VARCHAR NOT NULL, 
        PRIMARY KEY (id)
)


INFO Engine [no key 0.00033s] ()
INFO Engine 
CREATE TABLE hero (
        id INTEGER, 
        name VARCHAR NOT NULL, 
        secret_name VARCHAR NOT NULL, 
        age INTEGER, 
        PRIMARY KEY (id)
)


INFO Engine [no key 0.00016s] ()
INFO Engine 

// Our shinny new link table ✨
CREATE TABLE heroteamlink (
        team_id INTEGER, 
        hero_id INTEGER, 
        PRIMARY KEY (team_id, hero_id), 
        FOREIGN KEY(team_id) REFERENCES team (id), 
        FOREIGN KEY(hero_id) REFERENCES hero (id)
)


INFO Engine [no key 0.00031s] ()
INFO Engine COMMIT

```

</div>

## Recap

We can support **many-to-many** relationships between tables by declaring a link table.

We can create it the same way as with other **SQLModel** classes, and then use it in the `link_model` parameter to `Relationship()`.

Now let's work with data using these models in the next chapters. 🤓
