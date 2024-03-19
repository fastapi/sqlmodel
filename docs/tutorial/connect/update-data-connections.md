# Update Data Connections

At this point we have a `team` table:

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
<td>3</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>null</td>
</tr>
</table>

Some of these heroes are part of a team.

Now we'll see how to **update** those connections between rows tables.

We will continue with the code we used to create some heroes, and we'll update them.

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

## Assign a Team to a Hero

Let's say that **Tommy Sharp** uses his "rich uncle" charms to recruit **Spider-Boy** to join the team of the **Preventers**, now we need to update our Spider-Boy hero object to connect it to the Preventers team.

Doing it is just like updating any other field:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/connect/update/tutorial001_py310.py[ln:29-30]!}

        # Previous code here omitted 👈

{!./docs_src/tutorial/connect/update/tutorial001_py310.py[ln:60-64]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/connect/update/tutorial001.py[ln:31-32]!}

        # Previous code here omitted 👈

{!./docs_src/tutorial/connect/update/tutorial001.py[ln:62-66]!}

# Code below omitted 👇
```

////

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

We can simply **assign** a value to that field attribute `team_id`, then `add()` the hero to the session, and then `commit()`.

Next we `refresh()` it to get the recent data, and we print it.

Running that in the command line will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 😉

// Update the hero
INFO Engine UPDATE hero SET team_id=? WHERE hero.id = ?
INFO Engine [generated in 0.00014s] (1, 3)
// Commit the session saving the changes
INFO Engine COMMIT
// Automatically start a new transaction
INFO Engine BEGIN (implicit)
// Refresh the hero data
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age, hero.team_id
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.08837s ago] (3,)

// Print the updated hero
Updated hero: id=3 secret_name='Pedro Parqueador' team_id=1 name='Spider-Boy' age=None
```

</div>

And now **Spider-Boy** has the `team_id=1`, which is the ID of the Preventers. 🎉

Let's now see how to remove connections in the next chapter. 💥
