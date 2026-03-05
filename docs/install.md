# Install **SQLModel**

Create a project directory, create a [virtual environment](virtual-environments.md), activate it, and then install **SQLModel**, for example with:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
Successfully installed sqlmodel pydantic sqlalchemy
```

</div>

As **SQLModel** is built on top of [SQLAlchemy](https://www.sqlalchemy.org/) and [Pydantic](https://pydantic-docs.helpmanual.io/), when you install `sqlmodel` they will also be automatically installed.

## Install DB Browser for SQLite

Remember that [SQLite is a simple database in a single file](databases.md#a-single-file-database)?

For most of the tutorial I'll use SQLite for the examples.

Python has integrated support for SQLite, it is a single file read and processed from Python. And it doesn't need an [External Database Server](databases.md#a-server-database), so it will be perfect for learning.

In fact, SQLite is perfectly capable of handling quite big applications. At some point you might want to migrate to a server-based database like [PostgreSQL](https://www.postgresql.org/) (which is also free). But for now we'll stick to SQLite.

Through the tutorial I will show you SQL fragments, and Python examples. And I hope (and expect 🧐) you to actually run them, and verify that the database is working as expected and showing you the same data.

To be able to explore the SQLite file yourself, independent of Python code (and probably at the same time), I recommend you use [DB Browser for SQLite](https://sqlitebrowser.org/).

It's a great and simple program to interact with SQLite databases (SQLite files) in a nice user interface.

<img src="https://sqlitebrowser.org/images/screenshot.png">

Go ahead and [Install DB Browser for SQLite](https://sqlitebrowser.org/), it's free.

## Next Steps

Okay, let's get going! On the next section we'll start the [Tutorial - User Guide](tutorial/index.md). 🚀
