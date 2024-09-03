# Read Data - SELECT

We already have a database and a table with some data in it that looks more or less like this:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td>
</tr>
</table>

Things are getting more exciting! Let's now see how to read data from the database! 🤩

## Continue From Previous Code

Let's continue from the last code we used to create some data.

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial002_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial002.py!}
```

////

///

We are creating a **SQLModel** `Hero` class model and creating some records.

We will need the `Hero` model and the **engine**, but we will create a new session to query data in a new function.

## Read Data with SQL

Before writing Python code let's do a quick review of how querying data with SQL looks like:

```SQL
SELECT id, name, secret_name, age
FROM hero
```

It means, more or less:

> Hey SQL database 👋, please go and `SELECT` some data for me.
>
> I'll first tell you the columns I want:
>
> * `id`
> * `name`
> * `secret_name`
> * `age`
>
> And I want you to get them `FROM` the table called `"hero"`.

Then the database will go and get the data and return it to you in a table like this:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td>
</tr>
</table>

You can try that out in **DB Browser for SQLite**:

<img class="shadow" src="/img/tutorial/select/image01.png">

/// warning

Here we are getting all the rows.

If you have thousands of rows, that could be expensive to compute for the database.

You would normally want to filter the rows to receive only the ones you want. But we'll learn about that later in the next chapter.

///

### A SQL Shortcut

If we want to get all the columns like in this case above, in SQL there's a shortcut, instead of specifying each of the column names we could write a `*`:

```SQL
SELECT *
FROM hero
```

That would end up in the same result. Although we won't use that for **SQLModel**.

### `SELECT` Fewer Columns

We can also `SELECT` fewer columns, for example:

```SQL
SELECT id, name
FROM hero
```

Here we are only selecting the `id` and `name` columns.

And it would result in a table like this:

<table>
<tr>
<th>id</th><th>name</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td>
</tr>
</table>

And here is something interesting to notice. SQL databases store their data in tables. And they also always communicate their results in **tables**.

### `SELECT` Variants

The SQL language allows several **variations** in several places.

One of those variations is that in `SELECT` statements you can use the names of the columns directly, or you can prefix them with the name of the table and a dot.

For example, the same SQL code above could be written as:

```SQL
SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
```

This will be particularly important later when working with multiple tables at the same time that could have the same name for some columns.

For example `hero.id` and `team.id`, or `hero.name` and `team.name`.

Another variation is that most of the SQL keywords like `SELECT` can also be written in lowercase, like `select`.

### Result Tables Don't Have to Exist

This is the interesting part. The tables returned by SQL databases **don't have to exist** in the database as independent tables. 🧙

For example, in our database, we only have one table that has all the columns, `id`, `name`, `secret_name`, `age`. And here we are getting a result table with fewer columns.

One of the main points of SQL is to be able to keep the data structured in different tables, without repeating data, etc, and then query the database in many ways and get many different tables as a result.

## Read Data with **SQLModel**

Now let's do the same query to read all the heroes, but with **SQLModel**.

## Create a **Session**

The first step is to create a **Session**, the same way we did when creating the rows.

We will start with that in a new function `select_heroes()`:

//// tab | Python 3.10+

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001_py310.py[ln:34-35]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001.py[ln:36-37]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

## Create a `select` Statement

Next, pretty much the same way we wrote a SQL `SELECT` statement above, now we'll create a **SQLModel** `select` statement.

First we have to import `select` from `sqlmodel` at the top of the file:

//// tab | Python 3.10+

```Python hl_lines="1"
{!./docs_src/tutorial/select/tutorial001_py310.py[ln:1]!}

# More code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
{!./docs_src/tutorial/select/tutorial001.py[ln:1-3]!}

# More code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

And then we will use it to create a `SELECT` statement in Python code:

//// tab | Python 3.10+

```Python hl_lines="7"
{!./docs_src/tutorial/select/tutorial001_py310.py[ln:1]!}

# More code here omitted 👈

{!./docs_src/tutorial/select/tutorial001_py310.py[ln:34-36]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9"
{!./docs_src/tutorial/select/tutorial001.py[ln:1-3]!}

# More code here omitted 👈

{!./docs_src/tutorial/select/tutorial001.py[ln:36-38]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

It's a very simple line of code that conveys a lot of information:

```Python
statement = select(Hero)
```

This is equivalent to the first SQL `SELECT` statement above:

```SQL
SELECT id, name, secret_name, age
FROM hero
```

We pass the class model `Hero` to the `select()` function. And that tells it that we want to select all the columns necessary for the `Hero` class.

And notice that in the `select()` function we don't explicitly specify the `FROM` part. It is already obvious to **SQLModel** (actually to SQLAlchemy) that we want to select `FROM` the table `hero`, because that's the one associated with the `Hero` class model.

/// tip

The value of the `statement` returned by `select()` is a special object that allows us to do other things.

I'll tell you about that in the next chapters.

///

## Execute the Statement

Now that we have the `select` statement, we can execute it with the **session**:

//// tab | Python 3.10+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001_py310.py[ln:34-37]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="6"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001.py[ln:36-39]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

This will tell the **session** to go ahead and use the **engine** to execute that `SELECT` statement in the database and bring the results back.

Because we created the **engine** with `echo=True`, it will show the SQL it executes in the output.

This `session.exec(statement)` will generate this output:

```
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
INFO Engine [no key 0.00032s] ()
```

The database returns the table with all the data, just like above when we wrote SQL directly:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td>
</tr>
</table>

## Iterate Through the Results

The `results` object is an <abbr title="Something that can be used in a for loop">iterable</abbr> that can be used to go through each one of the rows.

Now we can put it in a `for` loop and print each one of the heroes:

//// tab | Python 3.10+

```Python hl_lines="7-8"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001_py310.py[ln:34-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7-8"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001.py[ln:36-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

This will print the output:

```
id=1 name='Deadpond' age=None secret_name='Dive Wilson'
id=2 name='Spider-Boy' age=None secret_name='Pedro Parqueador'
id=3 name='Rusty-Man' age=48 secret_name='Tommy Sharp'
```

## Add `select_heroes()` to `main()`

Now include a call to `select_heroes()` in the `main()` function so that it is executed when we run the program from the command line:

//// tab | Python 3.10+

```Python hl_lines="14"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001_py310.py[ln:34-45]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="14"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial001.py[ln:36-47]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial001.py!}
```

////

///

## Review The Code

Great, you're now being able to read the data from the database! 🎉

Let's review the code up to this point:

//// tab | Python 3.10+

```{ .python .annotate }
{!./docs_src/tutorial/select/tutorial002_py310.py!}
```

{!./docs_src/tutorial/select/annotations/en/tutorial002.md!}

////

//// tab | Python 3.7+

```{ .python .annotate }
{!./docs_src/tutorial/select/tutorial002.py!}
```

{!./docs_src/tutorial/select/annotations/en/tutorial002.md!}

////

/// tip

Check out the number bubbles to see what is done by each line of code.

///

Here it starts to become more evident why we should have a single **engine** for the whole application, but different **sessions** for each group of operations.

This new session we created uses the *same* **engine**, but it's a new and independent **session**.

The code above creating the models could, for example, live in a function handling web API requests and creating models.

And the second section reading data from the database could be in another function for other requests.

So, both sections could be in **different places** and would need their own sessions.

/// info

To be fair, in this example all that code could actually share the same **session**, there's actually no need to have two here.

But it allows me to show you how they could be separated and to reinforce the idea that you should have **one engine** per application, and **multiple sessions**, one per each group of operations.

///

## Get a List of `Hero` Objects

Up to now we are using the `results` to iterate over them.

But for different reasons you might want to have the full **list of `Hero`** objects right away instead of just an *iterable*. For example, if you want to return them in a web API.

The special `results` object also has a method `results.all()` that returns a list with all the objects:

//// tab | Python 3.10+

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial003_py310.py[ln:34-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="7"
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

With this now we have all the heroes in a list in the `heroes` variable.

After printing it, we would see something like:

```
[
    Hero(id=1, name='Deadpond', age=None, secret_name='Dive Wilson'),
    Hero(id=2, name='Spider-Boy', age=None, secret_name='Pedro Parqueador'),
    Hero(id=3, name='Rusty-Man', age=48, secret_name='Tommy Sharp')
]
```

/// info

It would actually look more compact, I'm formatting it a bit for you to see that it is actually a list with all the data.

///

## Compact Version

I have been creating several variables to be able to explain to you what each thing is doing.

But knowing what is each object and what it is all doing, we can simplify it a bit and put it in a more compact form:

//// tab | Python 3.10+

```Python  hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial004_py310.py[ln:34-37]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python  hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/select/tutorial004.py[ln:36-39]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/select/tutorial004_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/select/tutorial004.py!}
```

////

///

Here we are putting it all on a single line, you will probably put the select statements in a single line like this more often.

## SQLModel or SQLAlchemy - Technical Details

**SQLModel** is actually, more or less, just **SQLAlchemy** and **Pydantic** underneath, combined together.

It uses and returns the same types of objects and is compatible with both libraries.

Nevertheless, **SQLModel** defines a few of its own internal parts to improve the developer experience.

In this chapter we are touching some of them.

### SQLModel's `select`

When importing from `sqlmodel` the `select()` function, you are using **SQLModel**'s version of `select`.

SQLAchemy also has its own `select`, and SQLModel's `select` uses SQLAlchemy's `select` internally.

But SQLModel's version does a lot of **tricks** with type annotations to make sure you get the best **editor support** possible, no matter if you use **VS Code**, **PyCharm**, or something else. ✨

/// info

There was a lot of work and research, with different versions of the internal code, to improve this as much as possible. 🤓

///

### SQLModel's `session.exec`

📢 This is one to pay special attention to.

SQLAlchemy's own `Session` has a method `session.execute()`. It doesn't have a `session.exec()` method.

If you see SQLAlchemy tutorials, they will always use `session.execute()`.

**SQLModel**'s own `Session` inherits directly from SQLAlchemy's `Session`, and adds this additional method `session.exec()`. Underneath, it uses the same `session.execute()`.

But `session.exec()` does several **tricks** combined with the tricks in `session()` to give you the **best editor support**, with **autocompletion** and **inline errors** everywhere, even after getting data from a select. ✨

For example, in SQLAlchemy you would need to add a `.scalars()` here:

```Python
heroes = session.execute(select(Hero)).scalars().all()
```

But you would have to remove it when selecting multiple things (we'll see that later).

SQLModel's `session.exec()` takes care of that for you, so you don't have to add the `.scalars()`.

This is something that SQLAlchemy currently can't provide, because the regular `session.execute()` supports several other use cases, including legacy ones, so it can't have all the internal type annotations and tricks to support this.

On top of that, **SQLModel**'s `session.exec()` also does some tricks to reduce the amount of code you have to write and to make it as intuitive as possible.

But SQLModel's `Session` still has access to `session.execute()` too.

/// tip

Your editor will give you autocompletion for both `session.exec()` and `session.execute()`.

📢 Remember to **always use `session.exec()`** to get the best editor support and developer experience.

///

### Caveats of **SQLModel** Flavor

SQLModel is designed to have the best **developer experience** in a narrow set of **very common use cases**. ✨

You can still combine it with SQLAlchemy directly and use **all the features** of SQLAlchemy when you need to, including lower level more "pure" SQL constructs, exotic patterns, and even legacy ones. 🤓

But **SQLModel**'s design (e.g. type annotations) assume you are using it in the ways I explain here in the documentation.

Thanks to this, you will get as much **autocompletion** and **inline errors** as possible. 🚀

But this also means that if you use SQLModel with some more **exotic patterns** from SQLAlchemy, your editor might tell you that *there's an error*, while in fact, the code would still work.

That's the trade-off. 🤷

But for the situations where you need those exotic patterns, you can always use SQLAlchemy directly combined with SQLModel (using the same models, etc).
