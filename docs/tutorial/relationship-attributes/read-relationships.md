# Read Relationships

Now that we know how to connect data using **relationship Attributes**, let's see how to get and read the objects from a relationship.

## Select a Hero

First, add a function `select_heroes()` where we get a hero to start working with, and add that function to the `main()` function:

{* ./docs_src/tutorial/relationship_attributes/read_relationships/tutorial001_py310.py ln[94:98,108:111] hl[94:98,111] *}

## Select the Related Team - Old Way

Now that we have a hero, we can get the team this hero belongs to.

With what we have learned **up to now**, we could use a `select()` statement, then execute it with `session.exec()`, and then get the `.first()` result, for example:

{* ./docs_src/tutorial/relationship_attributes/read_relationships/tutorial001_py310.py ln[94:103] hl[100:103] *}

## Get Relationship Team - New Way

But now that we have the **relationship attributes**, we can just access them, and **SQLModel** (actually SQLAlchemy) will go and fetch the corresponding data from the database, and make it available in the attribute. ✨

So, the highlighted block above, has the same results as the block below:

{* ./docs_src/tutorial/relationship_attributes/read_relationships/tutorial001_py310.py ln[94:98,105] hl[105] *}

/// tip

The automatic data fetching will work as long as the starting object (in this case the `Hero`) is associated with an **open** session.

For example, here, **inside** a `with` block with a `Session` object.

///

## Get a List of Relationship Objects

And the same way, when we are working on the **many** side of the **one-to-many** relationship, we can get a list of of the related objects just by accessing the relationship attribute:

{* ./docs_src/tutorial/relationship_attributes/read_relationships/tutorial002_py310.py ln[94:100] hl[100] *}

That would print a list with all the heroes in the Preventers team:

<div class="termy">

```console
$ python app.py

// Automatically fetch the heroes
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age, hero.team_id AS hero_team_id
FROM hero
WHERE ? = hero.team_id
INFO Engine [cached since 0.8774s ago] (2,)

// Print the list of Preventers
Preventers heroes: [
    Hero(name='Rusty-Man', age=48, id=2, secret_name='Tommy Sharp', team_id=2),
    Hero(name='Spider-Boy', age=None, id=3, secret_name='Pedro Parqueador', team_id=2),
    Hero(name='Tarantula', age=32, id=6, secret_name='Natalia Roman-on', team_id=2),
    Hero(name='Dr. Weird', age=36, id=7, secret_name='Steve Weird', team_id=2),
    Hero(name='Captain North America', age=93, id=8, secret_name='Esteban Rogelios', team_id=2)
]
```

</div>

## Recap

With **relationship attributes** you can use the power of common Python objects to easily access related data from the database. 😎
