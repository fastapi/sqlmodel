# Manage migrations

SQLModel integrates [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage migrations and DB Schema.


## **SQLModel** Code - Models and Migrations

Now let's start with the SQLModel code.

We will start with the **simplest version**, with just heroes (no teams yet).

This is almost the same code as you start to know by heart:

```Python
{!./docs_src/tutorial/migrations/simple_hero_migration/models.py!}
```

Let's jump in your shell and init migrations:

<div class="termy">

```console
$ sqlmodel migrations init
Creating directory '/path/to/your/project/migrations' ...  done
Creating directory '/path/to/your/project/migrations/versions' ...  done
Generating /path/to/your/project/migrations/script.py.mako ...  done
Generating /path/to/your/project/migrations/env.py ...  done
Generating /path/to/your/project/migrations/README ...  done
Generating /path/to/your/project/alembic.ini ...  done
Adding '/path/to/your/project/migrations/__init__.py' ...  done
Adding '/path/to/your/project/migrations/versions/__init__.py' ...  done
Please edit configuration/connection/logging settings in '/path/to/your/project/alembic.ini' before proceeding.
```
</div>

Few things happended under the hood.

Let's review what happened: Below files just got created!

```hl_lines="5-12"
.
├── project
    ├── __init__.py
    ├── models.py
    ├── alembic.ini
    └── migrations
        ├── __init__.py
        ├── env.py
        ├── README
        ├── script.py.mako
        └── versions
            └── __init__.py
```

Let's review them step by step.

## Alembic configuration

**`alembic.ini`** gives all the details of Alembic's configuration. You shouldn't \*have to\* touch that a lot, but for our setup, we'll need to change few things.

We need to tell alembic how to connect to the database:

```ini hl_lines="10"
{!./docs_src/tutorial/migrations/simple_hero_migration/alembic001.ini[ln:1-5]!}

#.... Lot's of configuration!


{!./docs_src/tutorial/migrations/simple_hero_migration/alembic001.ini[ln:63]!} # 👈 Let's Change that!
```
Adapting our file, you will have:

```ini hl_lines="10"
{!./docs_src/tutorial/migrations/simple_hero_migration/alembic.ini[ln:1-5]!}

#.... Lot's of configuration!


{!./docs_src/tutorial/migrations/simple_hero_migration/alembic.ini[ln:63]!} # 👈 To that
```

For the full document, refer to [Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file)

**`./migrations/env.py`** is another file we'll need to configure:
It gives which Tables you want to migrate, let's open it and:

1. Import our models
2. Change `target_metadata` value

```Python hl_lines="5 7"
{!./docs_src/tutorial/migrations/simple_hero_migration/migrations/001.py[ln:1-5]!} 👈 Import your model
# .....
{!./docs_src/tutorial/migrations/simple_hero_migration/migrations/001.py[ln:19]!} 👈 Set you Metadata value
```

## Create an apply your first migration
!!! success
    👏🎉At this point, you are ready to track your DB Schema !

Let's create you first migration

<div class="termy">
```console
$ sqlmodel migrations init
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'hero'
  Generating /path/to/your/project/migrations/versions/0610946706a0_.py ...  done

```

</div>

Alembic did its magic and started to track your `Hero` model!
It created a new file `0610946706a0_.py`


```hl_lines="13"
.
└── project
    ├── __init__.py
    ├── models.py
    ├── alembic.ini
    └── migrations
        ├── __init__.py
        ├── env.py
        ├── README
        ├── script.py.mako
        └── versions
            ├── __init__.py
            └── 0610946706a0_.py
```

Let's prepare for our migration, and see what will happen.

<div class="termy">
```
$ sqlmodel migrations show
Rev: 50624637e300 (head)
Parent: <base>
Path: /path/to/your/project/migrations/versions/0610946706a0_.py #👈 That's our file

    empty message

    Revision ID: 50624637e300
    Revises:
    Create Date: 2023-10-31 19:40:22.084162
```
</div>

We are pretty sure about what will happen during migration, let's do it:

<div class="termy">
```
$ sqlmodel migrations upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 1e606859995a, migrating me iam famous
```
</div>


Let's open our DB browser and check it out:

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image008.png">



## Change you versions file name

Why the heck `0610946706a0_.py`?!!!!

The goal is to have a unique revision name to avoid collision.
In order to have a cleaner file name, we can edit `alembic.ini` and uncomment

```ini
{!./docs_src/tutorial/migrations/simple_hero_migration/alembic.ini[ln:11]!} #👈 Uncoment this line
```

Let's remove `0610946706a0_.py` and start it over.

<div class="termy">
```console
$ sqlmodel migrations revision
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'hero'
  Generating /path/to/your/project/migrations/versions//2023_10_31_1940-50624637e300_.py ...  done
```
</div>

Much better, not perfect but better.

To get more details just by looking at you file name, you can also run


<div class="termy">
```console
$ sqlmodel migrations revision "migrate me iam famous"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'hero'
  Generating /path/to/your/project/migrations/versions/2023_10_31_1946-1e606859995a_migrate_me_iam_famous.py
  ...  done
```
</div>


You can think of "migrate me iam famous" as a message you add to you migration.

It helps you keep track of what they do, pretty much like in `git`
