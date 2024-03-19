# Create Data with Many-to-Many Relationships

Let's continue from where we left and create some data.

We'll create data for this same **many-to-many** relationship with a link table:

<img alt="many-to-many table relationships" src="/img/tutorial/many-to-many/many-to-many.svg">

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

## Create Heroes

As we have done before, we'll create a function `create_heroes()` and we'll create some teams and heroes in it:

//// tab | Python 3.10+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py310.py[ln:36-54]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py39.py[ln:42-60]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:42-60]!}

# Code below omitted 👇
```

////

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

This is very similar to what we have done before.

We create a couple of teams, and then three heroes.

The only new detail is that instead of using an argument `team` we now use `teams`, because that is the name of the new **relationship attribute**. And more importantly, we pass a **list of teams** (even if it contains a single team).

See how **Deadpond** now belongs to the two teams?

## Commit, Refresh, and Print

Now let's do as we have done before, `commit` the **session**, `refresh` the data, and print it:

//// tab | Python 3.10+

```Python hl_lines="22-25  27-29  31-36"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py310.py[ln:36-69]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="22-25  27-29  31-36"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py39.py[ln:42-75]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="22-25  27-29  31-36"
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:42-75]!}

# Code below omitted 👇
```

////

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

## Add to Main

As before, add the `create_heroes()` function to the `main()` function to make sure it is called when running this program from the command line:

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py310.py[ln:72-74]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001_py39.py[ln:78-80]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/many_to_many/tutorial001.py[ln:78-80]!}

# Code below omitted 👇
```

////

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

## Run the Program

If we run the program from the command line, it would output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Automatically start a new transaction
INFO Engine BEGIN (implicit)
// Insert the hero data first
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [generated in 0.00041s] ('Deadpond', 'Dive Wilson', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001942s ago] ('Rusty-Man', 'Tommy Sharp', 48)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.002541s ago] ('Spider-Boy', 'Pedro Parqueador', None)
// Insert the team data second
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [generated in 0.00037s] ('Z-Force', 'Sister Margaret's Bar')
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [cached since 0.001239s ago] ('Preventers', 'Sharp Tower')
// Insert the link data last, to be able to re-use the created IDs
INFO Engine INSERT INTO heroteamlink (team_id, hero_id) VALUES (?, ?)
INFO Engine [generated in 0.00026s] ((2, 3), (1, 1), (2, 1), (2, 2))
// Commit and save the data in the database
INFO Engine COMMIT

// Automatically start a new transaction
INFO Engine BEGIN (implicit)
// Refresh the data
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00019s] (1,)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.001959s ago] (2,)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.003215s ago] (3,)

// Print Deadpond
Deadpond: name='Deadpond' age=None id=1 secret_name='Dive Wilson'

// Accessing the .team attribute triggers a refresh
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team, heroteamlink
WHERE ? = heroteamlink.hero_id AND team.id = heroteamlink.team_id
INFO Engine [generated in 0.00025s] (1,)

// Print Deadpond's teams, 2 teams! 🎉
Deadpond teams: [Team(id=1, name='Z-Force', headquarters='Sister Margaret's Bar'), Team(id=2, name='Preventers', headquarters='Sharp Tower')]

// Print Rusty-Man
Rusty-Man: name='Rusty-Man' age=48 id=2 secret_name='Tommy Sharp'

// Accessing the .team attribute triggers a refresh
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team, heroteamlink
WHERE ? = heroteamlink.hero_id AND team.id = heroteamlink.team_id
INFO Engine [cached since 0.001716s ago] (2,)

// Print Rusty-Man teams, just one, but still a list
Rusty-Man Teams: [Team(id=2, name='Preventers', headquarters='Sharp Tower')]

// Print Spider-Boy
Spider-Boy: name='Spider-Boy' age=None id=3 secret_name='Pedro Parqueador'

// Accessing the .team attribute triggers a refresh
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team, heroteamlink
WHERE ? = heroteamlink.hero_id AND team.id = heroteamlink.team_id
INFO Engine [cached since 0.002739s ago] (3,)

// Print Spider-Boy's teams, just one, but still a list
Spider-Boy Teams: [Team(id=2, name='Preventers', headquarters='Sharp Tower')]

// Automatic roll back any previous automatic transaction, at the end of the with block
INFO Engine ROLLBACK
```

</div>

## Recap

After setting up the model link, using it with **relationship attributes** is fairly straightforward, just Python objects. ✨
