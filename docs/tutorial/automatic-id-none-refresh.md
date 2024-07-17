# Automatic IDs, None Defaults, and Refreshing Data

In the previous chapter, we saw how to add rows to the database using **SQLModel**.

Now let's talk a bit about why the `id` field **can't be `NULL`** on the database because it's a **primary key**, and we declare it using `Field(primary_key=True)`.

But the same `id` field actually **can be `None`** in the Python code, so we declare the type with `int | None (or Optional[int])`, and set the default value to `Field(default=None)`:

//// tab | Python 3.10+

```Python hl_lines="4"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:4-8]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="4"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:6-10]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

Next, I'll show you a bit more about the synchronization of data between the database and the Python code.

When do we get an actual `int` from the database in that `id` field? Let's see all that. 👇

## Create a New `Hero` Instance

When we create a new `Hero` instance, we don't set the `id`:

//// tab | Python 3.10+

```Python hl_lines="3-6"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:21-24]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-6"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:23-26]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

### How `Optional` Helps

Because we don't set the `id`, it takes the Python's default value of `None` that we set in `Field(default=None)`.

This is the only reason why we define it with `Optional` and with a default value of `None`.

Because at this point in the code, **before interacting with the database**, the Python value could actually be `None`.

If we assumed that the `id` was *always* an `int` and added the type annotation without `Optional`, we could end up writing broken code, like:

```Python
next_hero_id = hero_1.id + 1
```

If we ran this code before saving the hero to the database and the `hero_1.id` was still `None`, we would get an error like:

```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

But by declaring it with `Optional[int]`, the editor will help us to avoid writing broken code by showing us a warning telling us that the code could be invalid if `hero_1.id` is `None`. 🔍

## Print the Default `id` Values

We can confirm that by printing our heroes before adding them to the database:

//// tab | Python 3.10+

```Python hl_lines="9-11"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:21-29]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9-11"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:23-31]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

That will output:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

Before interacting with the database
Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
```

</div>

Notice they all have `id=None`.

That's the default value we defined in the `Hero` model class.

What happens when we `add` these objects to the **session**?

## Add the Objects to the Session

After we add the `Hero` instance objects to the **session**, the IDs are *still* `None`.

We can verify by creating a session using a `with` block and adding the objects. And then printing them again:

//// tab | Python 3.10+

```Python hl_lines="19-21"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:21-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="19-21"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:23-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

This will, again, output the `id`s of the objects as `None`:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

After adding to the session
Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
```

</div>

As we saw before, the **session** is smart and doesn't talk to the database every time we prepare something to be changed, only after we are ready and tell it to `commit` the changes it goes and sends all the SQL to the database to store the data.

## Commit the Changes to the Database

Then we can `commit` the changes in the session, and print again:

//// tab | Python 3.10+

```Python hl_lines="13 16-18"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:31-46]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13 16-18"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:33-48]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

And now, something unexpected happens, look at the output, it seems as if the `Hero` instance objects had no data at all:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

// Here the engine talks to the database, the SQL part
INFO Engine BEGIN (implicit)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [generated in 0.00018s] ('Deadpond', 'Dive Wilson', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.0008968s ago] ('Spider-Boy', 'Pedro Parqueador', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001143s ago] ('Rusty-Man', 'Tommy Sharp', 48)
INFO Engine COMMIT

// And now our prints
After committing the session
Hero 1:
Hero 2:
Hero 3:

// What is happening here? 😱
```

</div>

What happens is that SQLModel (actually SQLAlchemy) is internally marking those objects as "expired", they **don't have the latest version of their data**. This is because we could have some fields updated in the database, for example, imagine a field `updated_at: datetime` that was automatically updated when we saved changes.

The same way, other values could have changed, so the option the **session** has to be sure and safe is to just internally mark the objects as expired.

And then, next time we access each attribute, for example with:

```Python
current_hero_name = hero_1.name
```

...SQLModel (actually SQLAlchemy) will make sure to contact the database and **get the most recent version of the data**, updating that field `name` in our object and then making it available for the rest of the Python expression. In the example above, at that point, Python would be able to continue executing and use that `hero_1.name` value (just updated) to put it in the variable `current_hero_name`.

All this happens automatically and behind the scenes. ✨

And here's the funny and strange thing with our example:

```Python
print("Hero 1:", hero_1)
```

We didn't access the object's attributes, like `hero.name`. We only accessed the entire object and printed it, so **SQLAlchemy has no way of knowing** that we want to access this object's data.

## Print a Single Field

To confirm and understand how this **automatic expiration and refresh** of data when accessing attributes work, we can print some individual fields (instance attributes):

//// tab | Python 3.10+

```Python hl_lines="21-23 26-28"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:31-56]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="21-23 26-28"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:33-58]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

Now we are actually accessing the attributes, because instead of printing the whole object `hero_1`:

```Python
print("Hero 1:", hero_1)
```

...we are now printing the `id` attribute in `hero.id`:

```Python
print("Hero 1 ID:", hero_1.id)
```

By accessing the attribute, that **triggers** a lot of work done by SQLModel (actually SQLAlchemy) underneath to **refresh the data from the database**, set it in the object's `id` attribute, and make it available for the Python expression (in this case just to print it).

Let's see how it works:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

// After committing, the objects are expired and have no values
After committing the session
Hero 1:
Hero 2:
Hero 3:

// Now we will access an attribute like the ID, this is the first print
After committing the session, show IDs

// Notice that before printing the first ID, the Session makes the Engine go to the database to refresh the data 🤓
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00017s] (1,)

// Here's our first print, now we have the database-generated ID
Hero 1 ID: 1

// Before the next print, refresh the data for the second object
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.001245s ago] (2,)

// Here's our print for the second hero with its auto-generated ID
Hero 2 ID: 2

// Before the third print, refresh its data
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.002215s ago] (3,)

// And here's our print for the third hero
Hero 3 ID: 3

// What if we print another attribute like the name?
After committing the session, show names
Hero 1 name: Deadpond
Hero 2 name: Spider-Boy
Hero 3 name: Rusty-Man

// Because the Session already refreshed these objects with all their data and the session knows they are not expired, it doesn't have to go again to the database for the names 🤓
```

</div>

## Refresh Objects Explicitly

You just learnt how the **session** refreshes the data automatically behind the scenes, as a side effect, when you access an attribute.

But what if you want to **explicitly refresh** the data?

You can do that too with `session.refresh(object)`:

//// tab | Python 3.10+

```Python hl_lines="30-32 35-37"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:31-65]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="30-32 35-37"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:33-67]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

When Python executes this code:

```Python
session.refresh(hero_1)
```

...the **session** goes and makes the **engine** communicate with the database to get the recent data for this object `hero_1`, and then the **session** puts the data in the `hero_1` object and marks it as "fresh" or "not expired".

Here's how the output would look like:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

// The first refresh
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00024s] (1,)

// The second refresh
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.001487s ago] (2,)

// The third refresh
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.002377s ago] (3,)

// Now print the data, as it's already refreshed there's no need for the Session to go and refresh it again
After refreshing the heroes
Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
```

</div>

This could be useful, for example, if you are building a web API to create heroes. And once a hero is created with some data, you return it to the client.

You wouldn't want to return an object that looks empty because the automatic magic to refresh the data was not triggered.

In this case, after committing the object to the database with the **session**, you could refresh it, and then return it to the client. This would ensure that the object has its fresh data.

## Print Data After Closing the Session

Now, as a final experiment, we can also print data after the **session** is closed.

There are no surprises here, it still works:

//// tab | Python 3.10+

```Python hl_lines="40-42"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py[ln:31-70]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="40-42"
# Code above omitted 👆

{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py[ln:33-72]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial001.py!}
```

////

///

And the output shows again the same data:

<div class="termy">

```console
$ python app.py

// Output above omitted 👆

// By finishing the with block, the Session is closed, including a rollback of any pending transaction that could have been there and was not committed
INFO Engine ROLLBACK

// Then we print the data, it works normally
After the session closes
Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
```

</div>

## Review All the Code

Now let's review all this code once again.

/// tip

Each one of the numbered bubbles shows what each line will print in the output.

And as we created the **engine** with `echo=True`, we can see the SQL statements being executed at each step.

///

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial002_py310.py!}
```

{!./docs_src/tutorial/automatic_id_none_refresh/annotations/en/tutorial002.md!}

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/automatic_id_none_refresh/tutorial002.py!}
```

{!./docs_src/tutorial/automatic_id_none_refresh/annotations/en/tutorial002.md!}

////

And here's all the output generated by running this program, all together:

<div class="termy">

```console
$ python app.py

INFO Engine BEGIN (implicit)
INFO Engine PRAGMA main.table_info("hero")
INFO Engine [raw sql] ()
INFO Engine PRAGMA temp.table_info("hero")
INFO Engine [raw sql] ()
INFO Engine
CREATE TABLE hero (
        id INTEGER,
        name VARCHAR NOT NULL,
        secret_name VARCHAR NOT NULL,
        age INTEGER,
        PRIMARY KEY (id)
)


INFO Engine [no key 0.00018s] ()
INFO Engine COMMIT
Before interacting with the database
Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
After adding to the session
Hero 1: id=None name='Deadpond' secret_name='Dive Wilson' age=None
Hero 2: id=None name='Spider-Boy' secret_name='Pedro Parqueador' age=None
Hero 3: id=None name='Rusty-Man' secret_name='Tommy Sharp' age=48
INFO Engine BEGIN (implicit)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [generated in 0.00022s] ('Deadpond', 'Dive Wilson', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001127s ago] ('Spider-Boy', 'Pedro Parqueador', None)
INFO Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO Engine [cached since 0.001483s ago] ('Rusty-Man', 'Tommy Sharp', 48)
INFO Engine COMMIT
After committing the session
Hero 1:
Hero 2:
Hero 3:
After committing the session, show IDs
INFO Engine BEGIN (implicit)
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00029s] (1,)
Hero 1 ID: 1
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.002132s ago] (2,)
Hero 2 ID: 2
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.003367s ago] (3,)
Hero 3 ID: 3
After committing the session, show names
Hero 1 name: Deadpond
Hero 2 name: Spider-Boy
Hero 3 name: Rusty-Man
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [generated in 0.00025s] (1,)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.001583s ago] (2,)
INFO Engine SELECT hero.id, hero.name, hero.secret_name, hero.age
FROM hero
WHERE hero.id = ?
INFO Engine [cached since 0.002722s ago] (3,)
After refreshing the heroes
Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
INFO Engine ROLLBACK
After the session closes
Hero 1: age=None id=1 name='Deadpond' secret_name='Dive Wilson'
Hero 2: age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
Hero 3: age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
```

</div>

## Recap

You read all that! That was a lot! Have some cake, you earned it. 🍰

We discussed how the **session** uses the **engine** to send SQL to the database, to create data and to fetch data too. How it keeps track of "**expired**" and "**fresh**" data. At which moments it **fetches data automatically** (when accessing instance attributes) and how that data is synchronized between objects in memory and the database via the **session**.

If you understood all that, now you know a lot about **SQLModel**, SQLAlchemy, and how the interactions from Python with databases work in general.

If you didn't get all that, it's fine, you can always come back later to <abbr title="See what I did there? 😜">`refresh`</abbr> the concepts.

I think this might be one of the main types of bugs that cause problems and makes you scratch your head. So, good job studying it! 💪
