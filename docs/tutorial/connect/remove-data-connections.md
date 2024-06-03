# Remove Data Connections

We currently have a `team` table:

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

And a `hero` table:

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
<td>3</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1</td>
</tr>
</table>

Let's see how to **remove** connections between rows in tables.

We will continue with the code from the previous chapter.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/update/tutorial001.py!}
```

////

///

## Break a Connection

We don't really have to delete anything to break a connection. We can just assign `None` to the foreign key, in this case, to the `team_id`.

Let's say **Spider-Boy** is tired of the lack of friendly neighbors and wants to get out of the **Preventers**.

We can simply set the `team_id` to `None`, and now it doesn't have a connection with the team:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/connect/delete/tutorial001_py310.py[ln:29-30]!}

        # Previous code here omitted 👈

{!./docs_src/tutorial/connect/delete/tutorial001_py310.py[ln:66-70]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/connect/delete/tutorial001.py[ln:31-32]!}

        # Previous code here omitted 👈

{!./docs_src/tutorial/connect/delete/tutorial001.py[ln:68-72]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/delete/tutorial001.py!}
```

////

///

Again, we just **assign** a value to that field attribute `team_id`, now the value is `None`, which means `NULL` in the database. Then we `add()` the hero to the session, and then `commit()`.

Next we `refresh()` it to get the recent data, and we print it.

Running that in the command line will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 😉

// Update the hero
INFO Engine UPDATE hero SET team_id=? WHERE hero.id = ?
INFO Engine [cached since 0.07753s ago] (None, 3)
// Commit the session
INFO Engine COMMIT
// Automatically start a new transaction
INFO Engine BEGIN (implicit)
// Refresh the hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.team_id
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.1661s ago] (3,)

// Print the hero without a team
No longer Preventer: id=3 secret_name='Pedro Parqueador' team_id=None name='Spider-Boy' age=None
```

</div>

That's it, we now removed a connection between rows in different tables by unsetting the foreign key column. 💥
