# Read a Range of Data - LIMIT and OFFSET

Now you know how to get a single row with `.one()`, `.first()`, and `session.get()`.

And you also know how to get multiple rows while filtering them using `.where()`.

Now let's see how to get only a **range of results**.

<img class="shadow" alt="table with first 3 rows selected" src="/img/tutorial/offset-and-limit/limit.svg">

## Create Data

We will continue with the same code as before, but we'll modify it a little the `select_heroes()` function to simplify the example and focus on what we want to achieve here.

Again, we will create several heroes to have some data to select from:

//// tab | Python 3.10+

```Python hl_lines="4-10"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial001_py310.py[ln:21-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="4-10"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial001.py[ln:23-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial001.py!}
```

////

///

## Review Select All

This is the code we had to select all the heroes in the `select()` examples:

//// tab | Python 3.10+

```Python hl_lines="3-8"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial003_py310.py[ln:34-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-8"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial003.py[ln:36-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial003_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial003.py!}
```

////

///

But this would get us **all** the heroes at the same time, in a database that could have thousands, that could be problematic.

## Select with Limit

We currently have 7 heroes in the database. But we could as well have thousands, so let's limit the results to get only the first 3:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial001_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial001.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial001.py!}
```

////

///

The special **select** object we get from `select()` also has a method `.limit()` that we can use to limit the results to a certain number.

In this case, instead of getting all the 7 rows, we are limiting them to only get the first 3.

<img class="shadow" alt="table with first 3 rows selected" src="/img/tutorial/offset-and-limit/limit.svg">

## Run the Program on the Command Line

If we run it on the command line, it will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Select with LIMIT
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
 LIMIT ? OFFSET ?
INFO Engine [no key 0.00014s] (3, 0)

// Print the heroes received, only 3
[
    Hero(age=None, secret_name='Dive Wilson', id=1, name='Deadpond'),
    Hero(age=None, secret_name='Pedro Parqueador', id=2, name='Spider-Boy'),
    Hero(age=48, secret_name='Tommy Sharp', id=3, name='Rusty-Man')
]
```

</div>

Great! We got only 3 heroes as we wanted.

/// tip

We will check out that SQL code more in a bit.

///

## Select with Offset and Limit

Now we can limit the results to get only the first 3.

But imagine we are in a user interface showing the results in batches of 3 heroes at a time.

/// tip

This is commonly called "pagination". Because the user interface would normally show a "page" of a predefined number of heroes at a time.

And then you can interact with the user interface to get the next page, and so on.

///

How do we get the next 3?

<img class="shadow" alt="table with next rows selected, from 4 to 6" src="/img/tutorial/offset-and-limit/limit2.svg">

We can use `.offset()`:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial002_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial002.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial002_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial002.py!}
```

////

///

The way this works is that the special **select** object we get from `select()` has methods like `.where()`, `.offset()` and `.limit()`.

Each of those methods applies the change in the internal special select statement object, and also **return the same object**, this way, we can continue using more methods on it, like in the example above that we use both `.offset()` and `.limit()`.

**Offset** means "skip this many rows", and as we want to skip the ones we already saw, the first three, we use `.offset(3)`.

## Run the Program with Offset on the Command Line

Now we can run the program on the command line, and it will output:

<div class="termy">

```console
$python app.py

// Previous output omitted 🙈

// Select with LIMIT and OFFSET
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
 LIMIT ? OFFSET ?
INFO Engine [no key 0.00020s] (3, 3)

// Print the 3 heroes received, the second batch
[
    Hero(age=32, secret_name='Natalia Roman-on', id=4, name='Tarantula'),
    Hero(age=35, secret_name='Trevor Challa', id=5, name='Black Lion'),
    Hero(age=36, secret_name='Steve Weird', id=6, name='Dr. Weird')
]
```

</div>

## Select Next Batch

Then to get the next batch of 3 rows we would offset all the ones we already saw, the first 6:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial003_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial003.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial003_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial003.py!}
```

////

///

The database right now has **only 7 rows**, so this query can only get 1 row.

<img class="shadow" alt="table with the last row (7th) selected" src="/img/tutorial/offset-and-limit/limit3.svg">

But don't worry, the database won't throw an error trying to get 3 rows when there's only one (as would happen with a Python list).

The database knows that we want to **limit** the number of results, but it doesn't necessarily have to find that many results.

## Run the Program with the Last Batch on the Command Line

And if we run it in the command line, it will output:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Select last batch with LIMIT and OFFSET
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
 LIMIT ? OFFSET ?
INFO Engine [no key 0.00038s] (3, 6)

// Print last batch of heroes, only one
[
    Hero(age=93, secret_name='Esteban Rogelios', id=7, name='Captain North America')
]
```

</div>

## SQL with LIMIT and OFFSET

You probably noticed the new SQL keywords `LIMIT` and `OFFSET`.

You can use them in SQL, at the end of the other parts:

```SQL
SELECT id, name, secret_name, age
FROM hero
LIMIT 3 OFFSET 6
```

If you try that in **DB Browser for SQLite**, you will get the same result:

<img class="shadow" alt="DB Browser for SQLite showing the result of the SQL query" src="/img/tutorial/offset-and-limit/db-browser.png">

## Combine Limit and Offset with Where

Of course, you can also combine `.limit()` and `.offset()` with `.where()` and other methods you will learn about later:

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial004_py310.py[ln:42-47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/offset_and_limit/tutorial004.py[ln:44-49]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial004_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/offset_and_limit/tutorial004.py!}
```

////

///

## Run the Program with Limit, Offset, and Where on the Command Line

If we run it on the command line, it will find all the heroes in the database with an age above 32. That would normally be 4 heroes.

But we are starting to include after an offset of 1 (so we don't count the first one), and we are limiting the results to only get the first 2 after that:

<div class="termy">

```console
$ python app.py

// Previous output omitted 🙈

// Select with WHERE and LIMIT and OFFSET
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.age > ?
 LIMIT ? OFFSET ?
INFO Engine [no key 0.00022s] (32, 2, 1)

// Print the heroes received, only 2
[
    Hero(age=36, id=6, name='Dr. Weird', secret_name='Steve Weird'),
    Hero(age=48, id=3, name='Rusty-Man', secret_name='Tommy Sharp')
]
```

</div>

## Recap

Independently of how you filter the data with `.where()` or other methods, you can limit the query to get at maximum some number of results with `.limit()`.

And the same way, you can skip the first results with `.offset()`.
