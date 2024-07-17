# Create Rows - Use the Session - INSERT

Now that we have a database and a table, we can start adding data.

Here's a reminder of how the table would look like, this is the data we want to add:

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

## Create Table and Database

We will continue from where we left of in the last chapter.

This is the code we had to create the database and table, nothing new here:

//// tab | Python 3.10+

```{.python .annotate hl_lines="20" }
{!./docs_src/tutorial/create_db_and_table/tutorial003_py310.py[ln:1-18]!}

# More code here later 👈

{!./docs_src/tutorial/create_db_and_table/tutorial003_py310.py[ln:21-22]!}
```

{!./docs_src/tutorial/create_db_and_table/annotations/en/tutorial003.md!}

////

//// tab | Python 3.7+

```{.python .annotate hl_lines="22" }
{!./docs_src/tutorial/create_db_and_table/tutorial003.py[ln:1-20]!}

# More code here later 👈

{!./docs_src/tutorial/create_db_and_table/tutorial003.py[ln:23-24]!}
```

{!./docs_src/tutorial/create_db_and_table/annotations/en/tutorial003.md!}

////

Now that we can create the database and the table, we will continue from this point and add more code on the same file to create the data.

## Create Data with SQL

Before working with Python code, let's see how we can create data with SQL.

Let's say we want to insert the record/row for `Deadpond` into our database.

We can do this with the following SQL code:

```SQL
INSERT INTO "hero" ("name", "secret_name")
VALUES ("Deadpond", "Dive Wilson");
```

It means, more or less:

> Hey SQL database 👋, please `INSERT` something (create a record/row) `INTO` the table `"hero"`.
>
> I want you to insert a row with some values in these specific columns:
>
> * `"name"`
> * `"secret_name"`
>
> And the values I want you to put in these columns are:
>
> * `"Deadpond"`
> * `"Dive Wilson"`

### Try it in DB Explorer for SQLite

You can try that SQL statement in **DB Explorer for SQLite**.

Make sure to open the same database we already created by clicking <kbd>Open Database</kbd> and selecting the same `database.db` file.

/// tip

If you don't have that `database.db` file with the table `hero`, you can re-create it by running the Python program at the top. 👆

///

Then go to the <kbd>Execute SQL</kbd> tab and copy the SQL from above.

It would look like this:

<img class="shadow" src="/img/tutorial/insert/image01.png">

Click the "Execute all" <kbd>▶</kbd> button.

Then you can go to the <kbd>Browse Data</kbd> tab, and you will see your newly created record/row:

<img class="shadow" src="/img/tutorial/insert/image02.png">

## Data in a Database and Data in Code

When working with a database (SQL or any other type) in a programming language, we will always have some data **in memory**, in objects and variables we create in our code, and there will be some data **in the database**.

We are constantly **getting** *some* of the data from the database and putting it in memory, in variables.

The same way, we are constantly **creating** variables and objects with data in our code, that we then want to save in the database, so we **send** it somehow.

In some cases, we can even create some data in memory and then change it and update it before saving it in the database.

We might even decide with some logic in the code that we no longer want to save the data in the database, and then just remove it. 🔥 And we only handled that data in memory, without sending it back and forth to the database.

**SQLModel** does all it can (actually via SQLAlchemy) to make this interaction as simple, intuitive, and familiar or "close to programming" as possible. ✨

But that division of the two places where some data might be at each moment in time (in memory or in the database) is always there. And it's important for you to have it in mind. 🤓

## Create Data with Python and **SQLModel**

Now let's create that same row in Python.

First, remove that file `database.db` so we can start from a clean slate.

Because we have Python code executing with data in memory, and the database is an independent system (an external SQLite file, or an external database server), we need to perform two steps:

* create the data in Python, in memory (in a variable)
* save/send the data to the database

## Create a Model Instance

Let's start with the first step, create the data in memory.

We already created a class `Hero` that represents the `hero` table in the database.

Each instance we create will represent the data in a row in the database.

So, the first step is to simply create an instance of `Hero`.

We'll create 3 right away, for the 3 heroes:

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial002_py310.py[ln:21-24]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial002.py[ln:23-26]!}

# More code here later 👇
```

////

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

/// tip

The code above in this file (the omitted code) is just the same code that you see at the top of this chapter.

The same code we used before to create the `Hero` model.

///

We are putting that in a function `create_heroes()`, to call it later once we finish it.

If you are trying the code interactively, you could also write that directly.

## Create a **Session**

Up to now, we have only used the **engine** to interact with the database.

The **engine** is that single object that we share with all the code, and that is in charge of communicating with the database, handling the connections (when using a server database like PostgreSQL or MySQL), etc.

But when working with **SQLModel** you will mostly use another tool that sits on top, the **Session**.

In contrast to the **engine** that is one for the whole application, we create a new **session** for each group of operations with the database that belong together.

In fact, the **session** needs and uses an **engine**.

For example, if we have a web application, we would normally have a single **session** per request.

We would re-use the same **engine** in all the code, everywhere in the application (shared by all the requests). But for each request, we would create and use a new **session**. And once the request is done, we would close the session.

The first step is to import the `Session` class:

//// tab | Python 3.10+

```Python hl_lines="1"
{!./docs_src/tutorial/insert/tutorial001_py310.py[ln:1]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
{!./docs_src/tutorial/insert/tutorial001.py[ln:1-3]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial001.py!}
```

////

///

Then we can create a new session:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial001_py310.py[ln:21-26]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial001.py[ln:23-28]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial001.py!}
```

////

///

The new `Session` takes an `engine` as a parameter. And it will use the **engine** underneath.

/// tip

We will see a better way to create a **session** using a `with` block later.

///

## Add Model Instances to the Session

Now that we have some hero model instances (some objects in memory) and a **session**, the next step is to add them to the session:

//// tab | Python 3.10+

```Python hl_lines="9-11"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial001_py310.py[ln:21-30]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9-11"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial001.py[ln:23-32]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial001.py!}
```

////

///

By this point, our heroes are *not* stored in the database yet.

And this is one of the cases where having a **session** independent of an **engine** makes sense.

The session is holding in memory all the objects that should be saved in the database later.

And once we are ready, we can **commit** those changes, and then the **session** will use the **engine** underneath to save all the data by sending the appropriate SQL to the database, and that way it will create all the rows. All in a single batch.

This makes the interactions with the database more efficient (plus some extra benefits).

/// info  | Technical Details

The session will create a new transaction and execute all the SQL code in that transaction.

This ensures that the data is saved in a single batch, and that it will all succeed or all fail, but it won't leave the database in a broken state.

///

## Commit the Session Changes

Now that we have the heroes in the **session** and that we are ready to save all that to the database, we can **commit** the changes:

//// tab | Python 3.10+

```Python hl_lines="13"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial001_py310.py[ln:21-32]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial001.py[ln:23-34]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial001.py!}
```

////

///

Once this line is executed, the **session** will use the **engine** to save all the data in the database by sending the corresponding SQL.

## Create Heroes as a Script

The function to create the heroes is now ready.

Now we just need to make sure to call it when we run this program with Python directly.

We already had a main block like:

```Python
if __name__ == "__main__":
    create_db_and_tables()
```

We could add the new function there, as:

```Python
if __name__ == "__main__":
    create_db_and_tables()
    create_heroes()
```

But to keep things a bit more organized, let's instead create a new function `main()` that will contain all the code that should be executed when called as an independent script, and we can put there the previous function `create_db_and_tables()`, and add the new function `create_heroes()`:

//// tab | Python 3.10+

```Python hl_lines="2  4"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002_py310.py[ln:34-36]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="2  4"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002.py[ln:36-38]!}

# More code here later 👇
```

////

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

And then we can call that single `main()` function from that main block:

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002_py310.py[ln:34-40]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002.py[ln:36-42]!}
```

////

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

By having everything that should happen when called as a script in a single function, we can easily add more code later on.

And some other code could also import and use this same `main()` function if it was necessary.

## Run the Script

Now we can run our program as a script from the console.

Because we created the **engine** with `echo=True`, it will print out all the SQL code that it is executing:

<div class="termy">

```console
$ python app.py
// Some boilerplate, checking that the hero table already exists
INFO Engine BEGIN (implicit)
INFO Engine PRAGMA main.table_info("hero")
INFO Engine [raw sql] ()
INFO Engine COMMIT
// BEGIN a transaction automatically ✨
INFO Engine BEGIN (implicit)
// Our INSERT statement, it uses VALUES (?, ?, ?) as parameters
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
// ...and these are the parameter values 🚀
INFO Engine [generated in 0.00013s] ('Deadpond', 'Dive Wilson', None)
// Again, for Spider-Boy
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.000755s ago] ('Spider-Boy', 'Pedro Parqueador', None)
// And now for Rusty-Man
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001014s ago] ('Rusty-Man', 'Tommy Sharp', 48)
// All good? Yes, commit this transaction! 🎉
INFO Engine COMMIT
```

</div>

If you have ever used Git, this works very similarly.

We use `session.add()` to add new objects (model instances) to the session (similar to `git add`).

And that ends up in a group of data ready to be saved, but not saved yet.

We can make more modifications, add more objects, etc.

And once we are ready, we can **commit** all the changes in a single step (similar to `git commit`).

## Close the Session

The **session** holds some resources, like connections from the engine.

So once we are done with the session, we should **close** it to make it release those resources and finish its cleanup:

//// tab | Python 3.10+

```Python hl_lines="16"
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial001_py310.py[ln:21-34]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="16"
# Code above omitted 👆

{!./docs_src/tutorial/insert/tutorial001.py[ln:23-36]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/insert/tutorial001.py!}
```

////

///

But what happens if we forget to close the session?

Or if there's an exception in the code and it never reaches the `session.close()`?

For that, there's a better way to create and close the session, using a `with` block. 👇

## A Session in a `with` Block

It's good to know how the `Session` works and how to create and close it manually. It might be useful if, for example, you want to explore the code in an interactive session (for example with Jupyter).

But there's a better way to handle the session, using a `with` block:

//// tab | Python 3.10+

```Python hl_lines="7-12"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002_py310.py[ln:21-31]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="7-12"
# Code above omitted 👆
{!./docs_src/tutorial/insert/tutorial002.py[ln:23-33]!}
```

////

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

This is the same as creating the session manually and then manually closing it. But here, using a `with` block, it will be automatically created when **starting** the `with` block and assigned to the variable `session`, and it will be automatically closed after the `with` block is **finished**.

And it will work even if there's an exception in the code. 😎

## Review All the Code

Let's give this whole file a final look. 🔍

You already know all the first part creating the `Hero` model class, the **engine**, and creating the database and table.

Let's focus on the new code:

//// tab | Python 3.10+

```{.python .annotate }
{!./docs_src/tutorial/insert/tutorial003_py310.py!}
```

{!./docs_src/tutorial/insert/annotations/en/tutorial003.md!}

////

//// tab | Python 3.7+

```{.python .annotate }
{!./docs_src/tutorial/insert/tutorial003.py!}
```

{!./docs_src/tutorial/insert/annotations/en/tutorial003.md!}

////

/// tip

Review what each line does by clicking each number bubble in the code. 👆

///

You can now put it in a `app.py` file and run it with Python. And you will see an output like the one shown above.

After that, if you open the database with **DB Browser for SQLite**, you will see the data you just created in the <kbd>Browse Data</kbd> tab:

<img class="shadow" src="/img/tutorial/insert/image03.png">

## What's Next

Now you know how to add rows to the database. 🎉

Now is a good time to understand better why the `id` field **can't be `NULL`** on the database because it's a **primary key**, but actually **can be `None`** in the Python code.

I'll tell you about that in the next chapter. 🚀
