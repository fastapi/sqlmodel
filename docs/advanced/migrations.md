# Migrations

We will use `Alembic` to handle database schema changes.

`SQLModel` is compatible with `Alembic`.  

## Initial example

We'll continue from another example that has the creation of database and tables, and other essentials features.

<details>
<summary>👀 Full file example</summary>

```Python
{!./docs_src/advanced/migrations/tutorial001.py!}
```

</details>

## First step

Add `Alembic` to your project.

Example using pip.

<div class="termy">

```console
$ pip install alembic

Installing collected packages: alembic
Successfully installed alembic-1.8.1
```

</div>

## Clean your code

We need to clean our step that create the database and tables.

```Python hl_lines="3-4"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial001.py[ln:19-20]!}

# Code below omitted 👇
```

```Python hl_lines="4-4"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial001.py[ln:44-47]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file example</summary>

```Python
{!./docs_src/advanced/migrations/main.py!}
```

</details>

## Alembic configuration

In this step we need initialize alembic.

<div class="termy">

```console
$ alembic init migrations

Creating directory migrations ...  done
Creating directory migrations\versions ...  done
Generating alembic.ini ...  done
Generating migrations\env.py ...  done
Generating migrations\README ...  done
Generating migrations\script.py.mako ...  done
Please edit configuration/connection/logging settings in 'alembic.ini' before proceeding.    

```

</div>

!!! info
    We can also use `alembic init alembic` to create `alembic` folder instead of `migrations` folder.

Then go to `migrations\script.py.mako` to add sqlmodel module.

```Python hl_lines="5-5"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial003.py[ln:8-10]!}

# Code below omitted 👇
```

!!! info
    In new migrations alembic will add SQLModel automatically.

<details>
<summary>👀 Full script.py.mako example</summary>

```Python
{!./docs_src/advanced/migrations/tutorial003.py!}
```

</details>

Then go to `migrations\env.py` to finish the alembic configuration.

- Import your models (in this case `Hero`) and `SQLModel`

```Python hl_lines="5-6"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial004.py[ln:1-6]!}

# Code below omitted 👇
```

!!! warning
    First import your models and then import SQLModel otherwise sqlmodel doesn´t recognize all models.

- Then set your database url

```Python hl_lines="4-4"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial004.py[ln:13-14]!}

# Code below omitted 👇
```

!!! tip
    This step can be replaced setting the same `sqlalchemy.url` variable in `alembic.ini` file.

- Finally set `target_metadata` with your `SQLModel.metada`

```Python hl_lines="3-3"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial004.py[ln:25-25]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full env.py example</summary>

```Python
{!./docs_src/advanced/migrations/tutorial004.py!}
```

</details>

## Run migrations

In this step we need to generate the initial version of the database.

<div class="termy">

```console
$ alembic revision --autogenerate -m "init_db"

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'hero'
Generating migrations\versions\34abfb7ac266_init_db.py ...  done
```

</div>

Now in `versions` folder we have a new file called `34abfb7ac266_init_db.py`

!!! info
    This file has a revision id and the message part from our revision command.

```{ .python .annotate }
{!./docs_src/advanced/migrations/tutorial005.py!}
```

{!./docs_src/advanced/migrations/annotations/en/tutorial005.md!}

!!! success
    At this moment we have all the files to create our new database model.

Initialize the database:

<div class="termy">

```console
$ alembic upgrade head

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.       
INFO  [alembic.runtime.migration] Running upgrade  -> 34abfb7ac266, init_db
```

</div>

Now we have two tables:

- `alembic_version`: with the version_num asociate with the revision id
- `hero`: the new table from our model

<img class="shadow" src="/img/advanced/migrations/migrations001.png">

`Hero` table is empty.

<img class="shadow" src="/img/advanced/migrations/migrations002.png">

Then run `main.py` script

<div class="termy">

```console
$ python main.py

INFO sqlalchemy.engine.Engine BEGIN (implicit)
INFO sqlalchemy.engine.Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO sqlalchemy.engine.Engine [generated in 0.00035s] ('Deadpond', 'Dive Wilson', None)
INFO sqlalchemy.engine.Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO sqlalchemy.engine.Engine [cached since 0.002439s ago] ('Spider-Boy', 'Pedro Parqueador', None)
INFO sqlalchemy.engine.Engine INSERT INTO hero (name, secret_name, age) VALUES (?, ?, ?)
INFO sqlalchemy.engine.Engine [cached since 0.003134s ago] ('Rusty-Man', 'Tommy Sharp', 48)      
INFO sqlalchemy.engine.Engine COMMIT
INFO sqlalchemy.engine.Engine BEGIN (implicit)
INFO sqlalchemy.engine.Engine SELECT hero.id, hero.name, hero.secret_name, hero.age 
FROM hero
INFO sqlalchemy.engine.Engine [generated in 0.00038s] ()
age=None id=1 name='Deadpond' secret_name='Dive Wilson'
age=None id=2 name='Spider-Boy' secret_name='Pedro Parqueador'
age=48 id=3 name='Rusty-Man' secret_name='Tommy Sharp'
INFO sqlalchemy.engine.Engine ROLLBACK
```

</div>

Now the `hero` table has new rows:

<img class="shadow" src="/img/advanced/migrations/migrations003.png">

## Next steps

If we edit our model changing the database schema we can run again alembic to generate a new revision.

Example: adding a new field named `power`

```Python hl_lines="4-4"
# Code above omitted 👆

{!./docs_src/advanced/migrations/tutorial006.py[ln:10-11]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file example</summary>

```Python
{!./docs_src/advanced/migrations/tutorial006.py!}
```

</details>

<div class="termy">

```console
$ alembic revision --autogenerate -m "new field power"

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'hero.power'
Generating migrations\versions\b39b8d3c77f0_new_field_power.py ...  done
```

</div>

The new file `b39b8d3c77f0_new_field_power.py`:

```{ .python .annotate }
{!./docs_src/advanced/migrations/tutorial007.py!}
```

{!./docs_src/advanced/migrations/annotations/en/tutorial007.md!}

!!! note
    Run `alembic upgrade head` to add the new field named power

<div class="termy">

```console
$ alembic upgrade head

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 357d6ebcfadf -> b39b8d3c77f0, new field power
```

</div>

!!! note
    After you can downgrade the database to the previous version, run `alembic downgrade -1`

<div class="termy">

```console
$ alembic downgrade -1

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade b39b8d3c77f0 -> 357d6ebcfadf, new field power
```

</div>

!!! success
    Migrations complete!!! Try adding new tables and relationship.
