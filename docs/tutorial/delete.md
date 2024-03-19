# Delete Data - DELETE

Now let's delete some data using **SQLModel**.

## Continue From Previous Code

As before, we'll continue from where we left off with the previous code.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial003_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial003.py!}
```

////

///

Remember to remove the `database.db` file before running the examples to get the same results.

## Delete with SQL

This `Spider-Youngster` is getting too weird, so let's just delete it.

But don't worry, we'll reboot it later with a new story. 😅

Let's see how to delete it with **SQL**:

```SQL hl_lines="1"
DELETE
FROM hero
WHERE name = "Spider-Youngster"
```

This means, more or less:

> Hey SQL database 👋, I want to `DELETE` rows `FROM` the table called `hero`.
>
> Please delete all the rows `WHERE` the value of the column `name` is equal to `"Spider-Youngster"`.

Remember that when using a `SELECT` statement it has the form:

```SQL
SELECT [some stuff here]
FROM [name of a table here]
WHERE [some condition here]
```

`DELETE` is very similar, and again we use `FROM` to tell the table to work on, and we use `WHERE` to tell the condition to use to match the rows that we want to delete.

You can try that in **DB Browser for SQLite**:

<img class="shadow" src="/img/tutorial/delete/image01.png">

Have in mind that `DELETE` is to delete entire **rows**, not single values in a row.

If you want to "delete" a single value in a column while **keeping the row**, you would instead **update** the row as explained in the previous chapter, setting the specific value of the column in that row to `NULL` (to `None` in Python).

Now let's delete with **SQLModel**.

To get the same results, delete the `database.db` file before running the examples.

## Read From the Database

We'll start by selecting the hero `"Spider-Youngster"` that we updated in the previous chapter, this is the one we will delete:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-75]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-77]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

As this is a new function `delete_heroes()`, we'll also add it to the `main()` function so that we call it when executing the program from the command line:

//// tab | Python 3.10+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:90-98]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:92-100]!}
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

That will print the same existing hero **Spider-Youngster**:

<div class="termy">

```console
$ python app.py

// Some boilerplate and previous output omitted 😉

// The SELECT with WHERE
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00011s] ('Spider-Youngster',)

// Print the hero as obtained from the database
Hero:  name='Spider-Youngster' secret_name='Pedro Parqueador' age=16 id=2
```

</div>

## Delete the Hero from the Session

Now, very similar to how we used `session.add()` to add or update new heroes, we can use `session.delete()` to delete the hero from the session:

//// tab | Python 3.10+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-77]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-79]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

## Commit the Session

To save the current changes in the session, **commit** it.

This will save all the changes stored in the **session**, like the deleted hero:

//// tab | Python 3.10+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-78]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-80]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

The same as we have seen before, `.commit()` will also save anything else that was added to the session. Including updates, or created heroes.

This commit after deleting the hero will generate this output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// The SQL to update the hero in the database
INFO Engine DELETE FROM hero WHERE hero.id = ?
INFO Engine [generated in 0.00020s] (2,)
INFO Engine COMMIT
```

</div>

## Print the Deleted Object

Now the hero is deleted from the database.

If we tried to use `session.refresh()` with it, it would raise an exception, because there's no data in the database for this hero.

Nevertheless, the object is still available with its data, but now it's not connected to the session and it no longer exists in the database.

As the object is not connected to the session, it is not marked as "expired", the session doesn't even care much about this object anymore.

Because of that, the object still contains its attributes with the data in it, so we can print it:

//// tab | Python 3.10+

```Python hl_lines="13"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-80]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-82]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

This will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// Print the deleted hero
Deleted hero: name='Spider-Youngster' secret_name='Pedro Parqueador' age=16 id=2
```

</div>

## Query the Database for the Same Row

To confirm if it was deleted, now let's query the database again, with the same `"Spider-Youngster"` name:

//// tab | Python 3.10+

```Python hl_lines="15-17"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-84]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="15-17"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-86]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

Here we are using `results.first()` to get the first object found (in case it found multiple) or `None`, if it didn't find anything.

If we used `results.one()` instead, it would raise an exception, because it expects exactly one result.

And because we just deleted that hero, this should not find anything and we should get `None`.

This will execute some SQL in the database and output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// Automatically start a new transaction
INFO Engine BEGIN (implicit)

// SQL to search for the hero
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00013s] ('Spider-Youngster',)
```

</div>

## Confirm the Deletion

Now let's just confirm that, indeed, no hero was found in the database with that name.

We'll do it by checking that the "first" item in the `results` is `None`:

//// tab | Python 3.10+

```Python hl_lines="19-20"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001_py310.py[ln:70-87]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="19-20"
# Code above omitted 👆

{!./docs_src/tutorial/delete/tutorial001.py[ln:72-89]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/delete/tutorial001.py!}
```

////

///

This will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// Indeed, the hero was deleted 🔥
There's no hero named Spider-Youngster

// Cleanup after the with block
INFO Engine ROLLBACK
```

</div>

## Review the Code

Now let's review all that code:

//// tab | Python 3.10+

```{ .python .annotate hl_lines="70-88" }
{!./docs_src/tutorial/delete/tutorial002_py310.py!}
```

{!./docs_src/tutorial/delete/annotations/en/tutorial002.md!}

////

//// tab | Python 3.7+

```{ .python .annotate hl_lines="72-90" }
{!./docs_src/tutorial/delete/tutorial002.py!}
```

{!./docs_src/tutorial/delete/annotations/en/tutorial002.md!}

////

/// tip

Check out the number bubbles to see what is done by each line of code.

///

## Recap

To delete rows with **SQLModel** you just have to `.delete()` them with the **session**, and then, as always, `.commit()` the session to save the changes to the database. 🔥
