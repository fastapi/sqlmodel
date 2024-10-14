# Read One Row

You already know how to filter rows to select using `.where()`.

And you saw how when executing a `select()` it normally returns an **iterable** object.

Or you can call `results.all()` to get a **list** of all the rows right away, instead of an iterable.

But in many cases you really just want to read a **single row**, and having to deal with an iterable or a list is not as convenient.

Let's see the utilities to read a single row.

## Continue From Previous Code

We'll continue with the same examples we have been using in the previous chapters to create and select data and we'll keep updating them.

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

If you already executed the previous examples and have a database with data, **remove the database file** before running each example, that way you won't have duplicate data and you will be able to get the same results.

## Read the First Row

We have been iterating over the rows in a `result` object like:

//// tab | Python 3.10+

```Python hl_lines="7-8"
# Code above omitted 👆

{!./docs_src/tutorial/indexes/tutorial002_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7-8"
# Code above omitted 👆

{!./docs_src/tutorial/indexes/tutorial002.py[ln:44-49]!}

# Code below omitted 👇
```

////

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

But let's say that we are not interested in all the rows, just the **first** one.

We can call the `.first()` method on the `results` object to get the first row:

//// tab | Python 3.10+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial001_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial001.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial001.py!}
```

////

///

This will return the first object in the `results` (if there was any).

That way, we don't have to deal with an iterable or a list.

/// tip

Notice that `.first()` is a method of the `results` object, not of the `select()` statement.

///

Although this query would find two rows, by using `.first()` we get only the first row.

If we run it in the command line it would output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// The SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.age <= ?
INFO Engine [no key 0.00021s] (35,)

// Only print the first item
Hero: secret_name='Natalia Roman-on' age=32 id=4 name='Tarantula'
```

</div>

## First or `None`

It would be possible that the SQL query doesn't find any row.

In that case, `.first()` will return `None`:

//// tab | Python 3.10+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial002_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial002.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial002_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial002.py!}
```

////

///

In this case, as there's no hero with an age less than 25, `.first()` will return `None`.

When we run it in the command line it will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// The SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.age <= ?
INFO Engine [no key 0.00021s] (35,)

// Now rows found, first is None
Hero: None
```

</div>

## Exactly One

There might be cases where we want to ensure that there's exactly **one** row matching the query.

And if there was more than one, it would mean that there's an error in the system, and we should terminate with an error.

In that case, instead of `.first()` we can use `.one()`:

//// tab | Python 3.10+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial003_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial003.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial003_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial003.py!}
```

////

///

Here we know that there's only one `"Deadpond"`, and there shouldn't be any more than one.

If we run it once will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// The SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00015s] ('Deadpond',)

// Only one row found, we're good ✅
Hero: secret_name='Dive Wilson' age=None id=1 name='Deadpond'
```

</div>

But if we run it again, as it will create and insert all the heroes in the database again, they will be duplicated, and there will be more than one `"Deadpond"`. 😱

So, running it again, without first deleting the file `database.db` will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// The SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.name = ?
INFO Engine [no key 0.00015s] ('Deadpond',)

// Oh, no, the database is in a broken state, with duplicates! 🚨
Traceback (most recent call last):

// Some details about the error omitted

sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when exactly one was required
```

</div>

## Exactly One with More Data

Of course, even if we don't duplicate the data, we could get the same error if we send a query that finds more than one row and expect exactly one with `.one()`:

//// tab | Python 3.10+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial004_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial004.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial004_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial004.py!}
```

////

///

That would find 2 rows, and would end up with the same error.

## Exactly One with No Data

And also, if we get no rows at all with `.one()`, it will also raise an error:

//// tab | Python 3.10+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial005_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial005.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial005_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial005.py!}
```

////

///

In this case, as there are no heroes with an age less than 25, `.one()` will raise an error.

This is what we would get if we run it in the command line:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// SELECT with WHERE
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.age < ?
INFO Engine [no key 0.00014s] (25,)

// Oh, no, we expected one row but there aren't any! 🚨
Traceback (most recent call last):

// Some details about the error omitted

sqlalchemy.exc.NoResultFound: No row was found when one was required
```

</div>

## Compact Version

Of course, with `.first()` and `.one()` you would also probably write all that in a more compact form most of the time, all in a single line (or at least a single Python statement):

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial006_py310.py[ln:42-45]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial006.py[ln:44-47]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial006_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial006.py!}
```

////

///

That would result in the same as some examples above.

## Select by Id with `.where()`

In many cases you might want to select a single row by its Id column with the **primary key**.

You could do it the same way we have been doing with a `.where()` and then getting the first item with `.first()`:

//// tab | Python 3.10+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial007_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5  7"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial007.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial007_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial007.py!}
```

////

///

That would work correctly, as expected. But there's a shorter version. 👇

## Select by Id with `.get()`

As selecting a single row by its Id column with the **primary key** is a common operation, there's a shortcut for it:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial008_py310.py[ln:42-45]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial008.py[ln:44-47]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial008_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial008.py!}
```

////

///

`session.get(Hero, 1)` is an equivalent to creating a `select()`, then filtering by Id using `.where()`, and then getting the first item with `.first()`.

If you run it, it will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// SELECT with WHERE
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00021s] (1,)

// The printed result
Hero: secret_name='Dive Wilson' age=None id=1 name='Deadpond'
```

</div>

## Select by Id with `.get()` with No Data

`.get()` behaves similar to `.first()`, if there's no data it will simply return `None` (instead of raising an error):

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial009_py310.py[ln:42-45]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/one/tutorial009.py[ln:44-47]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/one/tutorial009_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/one/tutorial009.py!}
```

////

///

Running that will output:

<div class="termy">

```console
$ python app.py

// Some boilerplate output omitted 😉

// SELECT with WHERE
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00024s] (9001,)

// No data found, so the value is None
Hero: None
```

</div>

## Recap

As querying the SQL database for a single row is a common operation, you now have several tools to do it in a short and simple way. 🎉
