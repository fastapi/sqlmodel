# Schema Migrations using Alembic

SQLModel integrates with [Alembic](https://alembic.sqlalchemy.org/) to handle schema migrations.
Alembic is a lightweight database migration tool for usage with SQLAlchemy.
Since SQLModel is built on top of SQLAlchemy, it's easy to use Alembic with SQLModel.

## Installation

To use Alembic with SQLModel, first install it:

<div class="termy">

```console
$ pip install alembic
---> 100%
Successfully installed alembic
```

</div>

Then, initialize Alembic in your project directory:

```console
alembic init migrations
```

This will create a directory named `migrations` and a configuration file named `alembic.ini`.

/// info

`migrations` is the directory where Alembic will store the migration scripts.
You can choose any other name for this directory, but `migrations` is a common convention.

///

## Integration

By making `class Table(SQLModel, table=true)`, you can add tables' information to SQLModel(SQLAlchemy) Metadata.

/// info

Metadata is a container object that keeps together many different features of a database.
You can access [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/core/metadata.html) for more information.

///

Import SQLModel on `./migrations/script.py.mako` and add the following code:

```python hl_lines="12"
{!./docs_src/advanced/migrations/tutorial001._py[ln:1-17]!}

# More code here later 👇
```

/// details | 👀 Full file preview

```Python hl_lines="12"
{!./docs_src/advanced/migrations/tutorial001._py!}
```

///

Next, load your models and set the target metadata on `./migrations/env.py`.

```python hl_lines="7  9  24"
{!./docs_src/advanced/migrations/tutorial002._py[ln:1-29]!}

(...)
```

Lastly, set the database connection string in `./alembic.ini`.

```python
# around line 63
sqlalchemy.url = driver://user:pass@localhost/dbname
```

## Revise and Upgrade

After setting up Alembic, you can create a new revision:

```console
alembic revision --autogenerate -m "create table"
```

This will create a new revision file in `./migrations/versions/`.

To apply the new revision and update the database schema, run:

```console
alembic upgrade head
```

/// tip

Remember to run `alembic upgrade head` to update the remote database's schema.

///
