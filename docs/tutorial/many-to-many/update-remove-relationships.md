# Update and Remove Many-to-Many Relationships

Now we'll see how to update and remove these **many-to-many** relationships.

We'll continue from where we left off with the previous code.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial001.py!}
```

////

///

## Get Data to Update

Let's now create a function `update_heroes()`.

We'll get **Spider-Boy** and the **Z-Force** team.

As you already know how these goes, I'll use the **short version** and get the data in a single Python statement.

And because we are now using `select()`, we also have to import it.

//// tab | Python 3.10+

```Python hl_lines="1  5-10"
{!./docs_src/tutorial/many_to_many/tutorial002_py310.py[ln:1]!}

# Some code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial002_py310.py[ln:72-77]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3  7-12"
{!./docs_src/tutorial/many_to_many/tutorial002_py39.py[ln:1-3]!}

# Some code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial002_py39.py[ln:78-83]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  7-12"
{!./docs_src/tutorial/many_to_many/tutorial002.py[ln:1-3]!}

# Some code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial002.py[ln:78-83]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002.py!}
```

////

///

And of course, we have to add `update_heroes()` to our `main()` function:

//// tab | Python 3.10+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py310.py[ln:94-101]!}
```

////

//// tab | Python 3.9+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py39.py[ln:100-107]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002.py[ln:100-107]!}
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002.py!}
```

////

///

## Add Many-to-Many Relationships

Now let's imagine that **Spider-Boy** thinks that the **Z-Force** team is super cool and decides to go there and join them.

We can use the same **relationship attributes** to include `hero_spider_boy` in the `team_z_force.heroes`.

//// tab | Python 3.10+

```Python hl_lines="10-12  14-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py310.py[ln:72-84]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="10-12  14-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py39.py[ln:78-90]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10-12  14-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002.py[ln:78-90]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002.py!}
```

////

///

/// tip

Because we are accessing an attribute in the models right after we commit, with `hero_spider_boy.teams` and `team_z_force.heroes`, the data is refreshed automatically.

So we don't have to call `session.refresh()`.

///

We then commit the change, refresh, and print the updated **Spider-Boy**'s heroes to confirm.

Notice that we only `add` **Z-Force** to the session, then we commit.

We never add **Spider-Boy** to the session, and we never even refresh it. But we still print his teams.

This still works correctly because we are using `back_populates` in the `Relationship()` in the models. That way, **SQLModel** (actually SQLAlchemy) can keep track of the changes and updates, and make sure they also happen on the relationships in the other related models. 🎉

## Run the Program

You can confirm it's all working by running the program in the command line:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Create the new many-to-many relationship
INFO Engine INSERT INTO heroteamlink (team_id, hero_id) VALUES (?, ?)
INFO Engine [generated in 0.00020s] (1, 3)
INFO Engine COMMIT

// Start a new automatic transaction
INFO Engine BEGIN (implicit)

// Automatically refresh the data while accessing the attribute .teams
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00044s] (3,)
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team, heroteamlink
WHERE ? = heroteamlink.hero_id AND team.id = heroteamlink.team_id
INFO Engine [cached since 0.1648s ago] (3,)

// Print Spider-Boy teams, including Z-Force 🎉
Updated Spider-Boy's Teams: [
    Team(id=2, name='Preventers', headquarters='Sharp Tower'),
    Team(id=1, name='Z-Force', headquarters='Sister Margaret's Bar')
]

// Automatically refresh the data while accessing the attribute .heores
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero, heroteamlink
WHERE ? = heroteamlink.team_id AND hero.id = heroteamlink.hero_id
INFO Engine [cached since 0.1499s ago] (1,)

// Print Z-Force heroes, including Spider-Boy 🎉
Z-Force heroes: [
    Hero(name='Deadpond', age=None, id=1, secret_name='Dive Wilson'),
    Hero(name='Spider-Boy', age=None, id=3, secret_name='Pedro Parqueador', teams=[
        Team(id=2, name='Preventers', headquarters='Sharp Tower'),
        Team(id=1, name='Z-Force', headquarters='Sister Margaret's Bar', heroes=[...])
    ])
]
```

</div>

## Remove Many-to-Many Relationships

Now let's say that right after joining the team, **Spider-Boy** realized that their "life preserving policies" are much more relaxed than what he's used to. 💀

And their *occupational safety and health* is also not as great... 💥

So, **Spider-Boy** decides to leave **Z-Force**.

Let's update the relationships to remove `team_z_force` from `hero_spider_boy.teams`.

Because `hero_spider_boy.teams` is just a list (a special list managed by SQLAlchemy, but a list), we can use the standard list methods.

In this case, we use the method `.remove()`, that takes an item and removes it from the list.

//// tab | Python 3.10+

```Python hl_lines="17-19  21-22"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py310.py[ln:72-91]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="17-19  21-22"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002_py39.py[ln:78-97]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="17-19  21-22"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial002.py[ln:78-97]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial002.py!}
```

////

///

And this time, just to show again that by using `back_populates` **SQLModel** (actually SQLAlchemy) takes care of connecting the models by their relationships, even though we performed the operation from the `hero_spider_boy` object (modifying `hero_spider_boy.teams`), we are adding `team_z_force` to the **session**. And we commit that, without even add `hero_spider_boy`.

This still works because by updating the teams in `hero_spider_boy`, because they are synchronized with `back_populates`, the changes are also reflected in `team_z_force`, so it also has changes to be saved in the DB (that **Spider-Boy** was removed).

And then we add the team, and commit the changes, which updates the `team_z_force` object, and because it changed the table that also had a connection with the `hero_spider_boy`, it is also marked internally as updated, so it all works.

And then we just print them again to confirm that everything worked correctly.

## Run the Program Again

To confirm that this last part worked, you can run the program again, it will output something like:

<div style="font-size: 1rem;" class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Delete the row in the link table
INFO Engine DELETE FROM heroteamlink WHERE heroteamlink.team_id = ? AND heroteamlink.hero_id = ?
INFO Engine [generated in 0.00043s] (1, 3)
// Save the changes
INFO Engine COMMIT

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// Automatically refresh the data while accessing the attribute .heroes
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [generated in 0.00029s] (1,)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero, heroteamlink
WHERE ? = heroteamlink.team_id AND hero.id = heroteamlink.hero_id
INFO Engine [cached since 0.5625s ago] (1,)

// Print the Z-Force heroes after reverting the changes
Reverted Z-Force's heroes: [
    Hero(name='Deadpond', age=None, id=1, secret_name='Dive Wilson')
]

// Automatically refresh the data while accessing the attribute .teams
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.4209s ago] (3,)
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team, heroteamlink
WHERE ? = heroteamlink.hero_id AND team.id = heroteamlink.team_id
INFO Engine [cached since 0.5842s ago] (3,)

// Print Spider-Boy's teams after reverting the changes
Reverted Spider-Boy's teams: [
    Team(id=2, name='Preventers', headquarters='Sharp Tower')
]

// Automatically roll back any possible previously unsaved transaction
INFO Engine ROLLBACK

```

</div>

## Recap

Updating and removing many-to-many relationships is quite straightforward after setting up the **link model** and the relationship attributes.

You can just use common list operation. 🚀
