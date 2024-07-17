# Create and Connect Rows

We will now **create rows** for each table. ✨

The `team` table will look like this:

<table>
<tr>
<th>id</th><th>name</th><th>headquarters</th>
</tr>
<tr>
<td>1</td><td>Preventers</td><td>Sharp Tower</td>
</tr>
<tr>
<td>2</td><td>Z-Force</td><td>Sister Margaret's Bar</td>
</tr>
</table>

And after we finish working with the data in this chapter, the `hero` table will look like this:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>2</td>
</tr>
<tr>
<td>2</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>1</td>
</tr>
<tr>
<td>3</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>null</td>
</tr>
</table>

Each row in the table `hero` will point to a row in the table `team`:

<img alt="table relationships" src="/img/tutorial/relationships/select/relationships2.svg">

/// info

We will later update **Spider-Boy** to add him to the **Preventers** team too, but not yet.

///

We will continue with the code in the previous example and we will add more things to it.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/create_tables/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/create_tables/tutorial001.py!}
```

////

///

Make sure you remove the `database.db` file before running the examples to get the same results.

## Create Rows for Teams with **SQLModel**

Let's do the same we did before and define a `create_heroes()` function where we create our heroes.

And now we will also create the teams there. 🎉

Let's start by creating two teams:

//// tab | Python 3.10+

```Python hl_lines="3-9"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:29-35]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-9"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:31-37]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

This would hopefully look already familiar.

We start a **session** in a `with` block using the same **engine** we created above.

Then we create two instances of the model class (in this case `Team`).

Next we add those objects to the **session**.

And finally we **commit** the session to save the changes to the database.

## Add It to Main

Let's not forget to add this function `create_heroes()` to the `main()` function so that we run it when calling the program from the command line:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:61-63]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:63-65]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

## Run it

If we run that code we have up to now, it will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 😉

// Automatically start a transaction
INFO Engine BEGIN (implicit)
// Add the teams to the database
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [generated in 0.00050s] ('Preventers', 'Sharp Tower')
INFO Engine INSERT INTO team (name, headquarters) VALUES (?, ?)
INFO Engine [cached since 0.002324s ago] ('Z-Force', 'Sister Margaret's Bar')
INFO Engine COMMIT
```

</div>

You can see in the output that it uses common SQL `INSERT` statements to create the rows.

## Create Rows for Heroes in Code

Now let's create one hero object to start.

As the `Hero` class model now has a field (column, attribute) `team_id`, we can set it by using the ID field from the `Team` objects we just created before:

//// tab | Python 3.10+

```Python hl_lines="12"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:29-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="12"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:31-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

We haven't committed this hero to the database yet, but there are already a couple of things to pay **attention** to.

If the database already had some teams, we wouldn't even know **what is the ID** that is going to be automatically assigned to each team by the database, for example, we couldn't just guess `1` or `2`.

But once the team is created and committed to the database, we can access the object's `id` field to get that ID.

Accessing an attribute in a model that was just committed, for example with `team_z_force.id`, automatically **triggers a refresh** of the data from the DB in the object, and then exposes the value for that field.

So, even though we are not committing this hero yet, just because we are using `team_z_force.id`, that will trigger some SQL sent to the database to fetch the data for this team.

That line alone would generate an output of:

```
INFO Engine BEGIN (implicit)
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [generated in 0.00025s] (2,)
```

Let's now create two more heroes:

//// tab | Python 3.10+

```Python hl_lines="14-20"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:29-50]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="14-20"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:31-52]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

When creating `hero_rusty_man`, we are accessing `team_preventers.id`, so that will also trigger a refresh of its data, generating an output of:

```
INFO Engine SELECT team.id AS team_id, team.name AS team_name, team.headquarters AS team_headquarters
FROM team
WHERE team.id = ?
INFO Engine [cached since 0.001795s ago] (1,)
```

There's something else to note. We marked `team_id` as `Optional[int]`, meaning that this could be `NULL` on the database (and `None` in Python).

That means that a hero doesn't have to have a team. And in this case, **Spider-Boy** doesn't have one.

Next we just commit the changes to save them to the database, and that will generate the output:

```
INFO Engine INSERT INTO hero (name, secret_name, age, team_id) VALUES (?, ?, ?, ?)
INFO Engine [generated in 0.00022s] ('Deadpond', 'Dive Wilson', None, 2)
INFO Engine INSERT INTO hero (name, secret_name, age, team_id) VALUES (?, ?, ?, ?)
INFO Engine [cached since 0.0007987s ago] ('Rusty-Man', 'Tommy Sharp', 48, 1)
INFO Engine INSERT INTO hero (name, secret_name, age, team_id) VALUES (?, ?, ?, ?)
INFO Engine [cached since 0.001095s ago] ('Spider-Boy', 'Pedro Parqueador', None, None)
INFO Engine COMMIT
```

## Refresh and Print Heroes

Now let's refresh and print those new heroes to see their new ID pointing to their teams:

//// tab | Python 3.10+

```Python hl_lines="26-28 30-32"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:29-58]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="26-28 30-32"
# Code above omitted 👆

{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:31-60]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

If we execute that in the command line, it will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 😉

// Automatically start a transaction
INFO Engine BEGIN (implicit)

// Refresh the first hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.team_id
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00021s] (1,)
// Refresh the second hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.team_id
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.001575s ago] (2,)
// Refresh the third hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.team_id
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.002518s ago] (3,)

// Print the heroes
Created hero: id=1 secret_name='Dive Wilson' team_id=2 name='Deadpond' age=None
Created hero: id=2 secret_name='Tommy Sharp' team_id=1 name='Rusty-Man' age=48
Created hero: id=3 secret_name='Pedro Parqueador' team_id=None name='Spider-Boy' age=None
```

</div>

They now have their `team_id`s, nice!

## Relationships

Relationships in SQL databases are just made by having **columns in one table** referencing the values in **columns on other tables**.

And here we have treated them just like that, more **column fields**, which is what they actually are behind the scenes in the SQL database.

But later in this tutorial, in the next group of chapters, you will learn about **Relationship Attributes** to make it all a lot easier to work with in code. ✨
