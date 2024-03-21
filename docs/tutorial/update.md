# Update Data - UPDATE

Now let's see how to update data using **SQLModel**.

## Continue From Previous Code

As before, we'll continue from where we left off with the previous code.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/indexes/tutorial002_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/indexes/tutorial002.py!}
```

////

///

Remember to remove the `database.db` file before running the examples to get the same results.

## Update with SQL

Let's quickly check how to update data with SQL:

```SQL hl_lines="1-2"
UPDATE hero
SET age=16
WHERE name = "Spider-Boy"
```

This means, more or less:

> Hey SQL database 👋, I want to `UPDATE` the table called `hero`.
>
> Please `SET` the value of the `age` column to `16`...
>
> ...for each of the rows `WHERE` the value of the column `name` is equal to `"Spider-Boy"`.

In a similar way to `SELECT` statements, the first part defines the columns to work with: what are the columns that have to be updated and to which value. The rest of the columns stay as they were.

And the second part, with the `WHERE`, defines to which rows it should apply that update.

In this case, as we only have one hero with the name `"Spider-Boy"`, it will only apply the update in that row.

/// info

Notice that in the `UPDATE` the single equals sign (`=`) means **assignment**, setting a column to some value.

And in the `WHERE` the same single equals sign (`=`) is used for **comparison** between two values, to find rows that match.

This is in contrast to Python and most programming languages, where a single equals sign (`=`) is used for assignment, and two equal signs (`==`) are used for comparisons.

///

You can try that in **DB Browser for SQLite**:

<img class="shadow" src="/img/tutorial/update/image01.png">

After that update, the data in the table will look like this, with the new age for Spider-Boy:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>16 ✨</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td>
</tr>
</table>

/// tip

It will probably be more common to find the row to update by `id`, for example:

```SQL
UPDATE hero
SET age=16
WHERE id = 2
```

But in the example above I used `name` to make it more intuitive.

///

Now let's do the same update in code, with **SQLModel**.

To get the same results, delete the `database.db` file before running the examples.

## Read From the Database

We'll start by selecting the hero `"Spider-Boy"`, this is the one we will update:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

Let's not forget to add that `update_heroes()` function to the `main()` function so that we call it when executing the program from the command line:

//// tab | Python 3.10+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:56-63]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:58-65]!}
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

Up to that point, running that in the command line will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate and previous output omitted 😉

// The SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00017s] ('Spider-Boy',)

// Print the hero as obtained from the database
Hero: name='Spider-Boy' secret_name='Pedro Parqueador' age=None id=2
```

</div>

/// tip

Notice that by this point, the hero still doesn't have an age.

///

## Set a Field Value

Now that you have a `hero` object, you can simply set the value of the field (the attribute representing a column) that you want.

In this case, we will set the `age` to `16`:

//// tab | Python 3.10+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-49]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-51]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

## Add the Hero to the Session

Now that the hero object in memory has a change, in this case a new value for the `age`, we need to add it to the session.

This is the same we did when creating new hero instances:

//// tab | Python 3.10+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-50]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-52]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

## Commit the Session

To save the current changes in the session, **commit** it.

This will save the updated hero in the database:

//// tab | Python 3.10+

```Python hl_lines="12"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-51]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="12"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-53]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

It will also save anything else that was added to the session.

For example, if you were also creating new heroes and had added those objects to the session before, they would now be saved too in this single commit.

This commit will generate this output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// The SQL to update the hero in the database
INFO Engine UPDATE hero SET age=? WHERE hero.id = ?
INFO Engine [generated in 0.00017s] (16, 2)
INFO Engine COMMIT
```

</div>

## Refresh the Object

At this point, the hero is updated in the database and it has the new data saved there.

The data in the object would be automatically refreshed if we accessed an attribute, like `hero.name`.

But in this example we are not accessing any attribute, we will only print the object. And we also want to be explicit, so we will `.refresh()` the object directly:

//// tab | Python 3.10+

```Python hl_lines="13"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-52]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-54]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

This refresh will trigger the same SQL query that would be automatically triggered by accessing an attribute. So it will generate this output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// The SQL to SELECT the fresh hero data
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00018s] (2,)
```

</div>

## Print the Updated Object

Now we can just print the hero:

//// tab | Python 3.10+

```Python hl_lines="14"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001_py310.py[ln:42-53]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="14"
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial001.py[ln:44-55]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial001.py!}
```

////

///

Because we refreshed it right after updating it, it has fresh data, including the new `age` we just updated.

So, printing it will show the new `age`:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// Previous output omitted 🙈

// Print the hero with the new age
Updated hero: name='Spider-Boy' secret_name='Pedro Parqueador' age=16 id=2
```

</div>

## Review the Code

Now let's review all that code:

//// tab | Python 3.10+

```{ .python .annotate hl_lines="42-53" }
{!./docs_src/tutorial/update/tutorial002_py310.py!}
```

{!./docs_src/tutorial/update/annotations/en/tutorial002.md!}

////

//// tab | Python 3.7+

```{ .python .annotate hl_lines="44-55" }
{!./docs_src/tutorial/update/tutorial002.py!}
```

{!./docs_src/tutorial/update/annotations/en/tutorial002.md!}

////

/// tip

Check out the number bubbles to see what is done by each line of code.

///

## Multiple Updates

The update process with **SQLModel** is more or less the same as with creating new objects, you add them to the session, and then commit them.

This also means that you can update several fields (attributes, columns) at once, and you can also update several objects (heroes) at once:

//// tab | Python 3.10+

```{ .python .annotate hl_lines="15-17  19-21  23" }
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial004_py310.py[ln:42-68]!}

# Code below omitted 👇
```

{!./docs_src/tutorial/update/annotations/en/tutorial004.md!}

////

//// tab | Python 3.7+

```{ .python .annotate hl_lines="15-17  19-21  23" }
# Code above omitted 👆

{!./docs_src/tutorial/update/tutorial004.py[ln:44-70]!}

# Code below omitted 👇
```

{!./docs_src/tutorial/update/annotations/en/tutorial004.md!}

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/update/tutorial004_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/update/tutorial004.py!}
```

////

///

/// tip

Review what each line does by clicking each number bubble in the code. 👆

///

## Recap

Update **SQLModel** objects just as you would with other Python objects. 🐍

Just remember to `add` them to a **session**, and then `commit` it. And if necessary, `refresh` them.
