# Link Model with Extra Fields

In the previous example we never interacted directly with the `HeroTeamLink` model, it was all through the automatic **many-to-many** relationship.

But what if we needed to have additional data to describe the link between the two models?

Let's say that we want to have an extra field/column to say if a hero **is still training** in that team or if they are already going on missions and stuff.

Let's see how to achieve that.

## Link Model with Two One-to-Many

The way to handle this is to explicitly use the link model, to be able to get and modify its data (apart from the foreign keys pointing to the two models for `Hero` and `Team`).

In the end, the way it works is just like two **one-to-many** relationships combined.

A row in the table `heroteamlink` points to **one** particular hero, but a single hero can be connected to **many** hero-team links, so it's **one-to-many**.

And also, the same row in the table `heroteamlink` points to **one** team, but a single team can be connected to **many** hero-team links, so it's also **one-to-many**.

/// tip

The previous many-to-many relationship was also just two one-to-many relationships combined, but now it's going to be much more explicit.

///

## Update Link Model

Let's update the `HeroTeamLink` model.

We will add a new field `is_training`.

And we will also add two **relationship attributes**, for the linked `team` and `hero`:

//// tab | Python 3.10+

```Python hl_lines="6  8-9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:4-10]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="10  12-13"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:6-16]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10  12-13"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:6-16]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

The new **relationship attributes** have their own `back_populates` pointing to new relationship attributes we will create in the `Hero` and `Team` models:

* `team`: has `back_populates="hero_links"`, because in the `Team` model, the attribute will contain the links to the **team's heroes**.
* `hero`: has `back_populates="team_links"`, because in the `Hero` model, the attribute will contain the links to the **hero's teams**.

/// info

In SQLAlchemy this is called an Association Object or Association Model.

I'm calling it **Link Model** just because that's easier to write avoiding typos. But you are also free to call it however you want. 😉

///

## Update Team Model

Now let's update the `Team` model.

We no longer have the `heroes` relationship attribute, and instead we have the new `hero_links` attribute:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:13-18]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:19-24]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:19-24]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

## Update Hero Model

The same with the `Hero` model.

We change the `teams` relationship attribute for `team_links`:

//// tab | Python 3.10+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:21-27]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:27-33]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:27-33]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

## Create Relationships

Now the process to create relationships is very similar.

But now we create the **explicit link models** manually, pointing to their hero and team instances, and specifying the additional link data (`is_training`):

//// tab | Python 3.10+

```Python hl_lines="21-30  32-35"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:40-79]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="21-30  32-35"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:46-85]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="21-30  32-35"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:46-85]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

We are just adding the link model instances to the session, because the link model instances are connected to the heroes and teams, they will be also automatically included in the session when we commit.

## Run the Program

Now, if we run the program, it will show almost the same output as before, because it is generating almost the same SQL, but this time including the new `is_training` column:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// Insert the heroes
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [generated in 0.00025s] ('Deadpond', 'Dive Wilson', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.00136s ago] ('Spider-Boy', 'Pedro Parqueador', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001858s ago] ('Rusty-Man', 'Tommy Sharp', 48)

// Insert the teams
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [generated in 0.00019s] ('Z-Force', 'Sister Margaret's Bar')
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [cached since 0.0007985s ago] ('Preventers', 'Sharp Tower')

// Insert the hero-team links
INFO Engine INSERT INTO heroteamlink (team_id, hero_id, is_training) VALUES (?, ?, ?)
INFO Engine [generated in 0.00023s] ((1, 1, 0), (2, 1, 1), (2, 2, 1), (2, 3, 0))
// Save the changes in the transaction in the database
INFO Engine COMMIT

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// Automatically fetch the data on attribute access
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [generated in 0.00028s] (1,)
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.team_id
INFO Engine [generated in 0.00026s] (1,)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00024s] (1,)

// Print Z-Force hero data, including link data
Z-Force hero: name='Deadpond' age=None id=1 secret_name='Dive Wilson' is training: False

// Automatically fetch the data on attribute access
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [cached since 0.008822s ago] (2,)
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.team_id
INFO Engine [cached since 0.005778s ago] (2,)

// Print Preventers hero data, including link data
Preventers hero: name='Deadpond' age=None id=1 secret_name='Dive Wilson' is training: True

// Automatically fetch the data on attribute access
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.004196s ago] (2,)

// Print Preventers hero data, including link data
Preventers hero: name='Spider-Boy' age=None id=2 secret_name='Pedro Parqueador' is training: True

// Automatically fetch the data on attribute access
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.006005s ago] (3,)

// Print Preventers hero data, including link data
Preventers hero: name='Rusty-Man' age=48 id=3 secret_name='Tommy Sharp' is training: False
```

</div>

## Add Relationships

Now, to add a new relationship, we have to create a new `HeroTeamLink` instance pointing to the hero and the team, add it to the session, and commit it.

Here we do that in the `update_heroes()` function:

//// tab | Python 3.10+

```Python hl_lines="10-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:82-97]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="10-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:88-103]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10-15"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:88-103]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

## Run the Program with the New Relationship

If we run that program, we will see the output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// Select the hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00014s] ('Spider-Boy',)

// Select the team
INFO Engine SELECT team.id, team.name, team.headquarters
FROM team
WHERE team.name = ?
INFO Engine [no key 0.00012s] ('Z-Force',)

// Create the link
INFO Engine INSERT INTO heroteamlink (team_id, hero_id, is_training) VALUES (?, ?, ?)
INFO Engine [generated in 0.00023s] (1, 2, 1)

// Automatically refresh the data on attribute access
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.team_id
INFO Engine [cached since 0.01514s ago] (1,)
INFO Engine COMMIT
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.08953s ago] (2,)
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.hero_id
INFO Engine [generated in 0.00018s] (2,)

// Print updated hero links
Updated Spider-Boy's Teams: [
    HeroTeamLink(team_id=2, is_training=True, hero_id=2),
    HeroTeamLink(team_id=1, is_training=True, hero_id=2)
]

// Automatically refresh team data on attribute access
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [cached since 0.1084s ago] (1,)
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.team_id
INFO Engine [cached since 0.1054s ago] (1,)

// Print team hero links
Z-Force heroes: [
    HeroTeamLink(team_id=1, is_training=False, hero_id=1),
    HeroTeamLink(team_id=1, is_training=True, hero_id=2)
]
```

</div>

## Update Relationships with Links

Now let's say that **Spider-Boy** has been training enough in the **Preventers**, and they say he can join the team full time.

So now we want to update the status of `is_training` to `False`.

We can do that by iterating on the links:

//// tab | Python 3.10+

```Python hl_lines="8-10"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:82-83]!}

        # Code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial003_py310.py[ln:99-107]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8-10"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:88-89]!}

        # Code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial003_py39.py[ln:105-113]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8-10"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:88-89]!}

        # Code here omitted 👈

{!./docs_src/tutorial/many_to_many/tutorial003.py[ln:105-113]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/many_to_many/tutorial003.py!}
```

////

///

## Run the Program with the Updated Relationships

And if we run the program now, it will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Automatically fetch team data on attribute access
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [generated in 0.00015s] (2,)

// Update link row
INFO Engine UPDATE heroteamlink SET is_training=? WHERE heroteamlink.team_id = ? AND heroteamlink.hero_id = ?
INFO Engine [generated in 0.00020s] (0, 2, 2)

// Save current transaction to database
INFO Engine COMMIT

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// Automatically fetch data on attribute access
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.2004s ago] (2,)
INFO Engine SELECT heroteamlink.team_id AS heroteamlink_team_id, heroteamlink.hero_id AS heroteamlink_hero_id, heroteamlink.is_training AS heroteamlink_is_training
FROM heroteamlink
WHERE ? = heroteamlink.hero_id
INFO Engine [cached since 0.1005s ago] (2,)
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [cached since 0.09707s ago] (2,)

// Print Spider-Boy team, including link data, if is training
Spider-Boy team: headquarters='Sharp Tower' id=2 name='Preventers' is training: False

// Automatically fetch data on attribute access
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [cached since 0.2097s ago] (1,)

// Print Spider-Boy team, including link data, if is training
Spider-Boy team: headquarters='Sister Margaret's Bar' id=1 name='Z-Force' is training: True
INFO Engine ROLLBACK
```

</div>

## Recap

If you need to store more information about a **many-to-many** relationship you can use an explicit link model with extra data in it. 🤓
