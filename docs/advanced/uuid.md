# UUID (Universally Unique Identifiers)

We have discussed some data types like `str`, `int`, etc.

There's another data type called `UUID` (Universally Unique Identifier).

You might have seen **UUIDs**, for example in URLs. They look something like this:

```
4ff2dab7-bffe-414d-88a5-1826b9fea8df
```

UUIDs can be particularly useful as an alternative to auto-incrementing integers for **primary keys**.

/// info

Official support for UUIDs was added in SQLModel version `0.0.20`.

///

## About UUIDs

UUIDs are numbers with 128 bits, that is, 16 bytes.

They are normally seen as 32 <abbr title="numbers in base 16 (instead of base 10), using letters from A to F to represent the numbers from 10 to 15">hexadecimal</abbr> characters separated by dashes.

There are several versions of UUID, some versions include the current time in the bytes, but **UUIDs version 4** are mainly random, the way they are generated makes them virtually **unique**.

### Distributed UUIDs

You could generate one UUID in one computer, and someone else could generate another UUID in another computer, and it would be almost **impossible** for both UUIDs to be the **same**.

This means that you don't have to wait for the DB to generate the ID for you, you can **generate it in code before sending it to the database**, because you can be quite certain it will be unique.

/// note | Technical Details

Because the number of possible UUIDs is so large (2^128), the probability of generating the same UUID version 4 (the random ones) twice is very low.

If you had 103 trillion version 4 UUIDs stored in the database, the probability of generating a duplicated new one is one in a billion. 🤓

///

For the same reason, if you decided to migrate your database, combine it with another database and mix records, etc. you would most probably be able to **just use the same UUIDs** you had originally.

/// warning

There's still a chance you could have a collision, but it's very low. In most cases you could assume you wouldn't have it, but it would be good to be prepared for it.

///

### UUIDs Prevent Information Leakage

Because UUIDs version 4 are **random**, you could give these IDs to the application users or to other systems, **without exposing information** about your application.

When using **auto-incremented integers** for primary keys, you could implicitly expose information about your system. For example, someone could create a new hero, and by getting the hero ID `20` **they would know that you have 20 heroes** in your system (or even less, if some heroes were already deleted).

### UUID Storage

Because UUIDs are 16 bytes, they would **consume more space** in the database than a smaller auto-incremented integer (commonly 4 bytes).

Depending on the database you use, UUIDs could have **better or worse performance**. If you are concerned about that, you should check the documentation for the specific database.

SQLite doesn't have a specific UUID type, so it will store the UUID as a string. Other databases like Postgres have a specific UUID type which would result in better performance and space usage than strings.

## Models with UUIDs

To use UUIDs as primary keys we need to import `uuid`, which is part of the Python standard library (we don't have to install anything) and use `uuid.UUID` as the **type** for the ID field.

We also want the Python code to **generate a new UUID** when creating a new instance, so we use `default_factory`.

The parameter `default_factory` takes a function (or in general, a "<abbr title="Something that can be called as a function.">callable</abbr>"). This function will be **called when creating a new instance** of the model and the value returned by the function will be used as the default value for the field.

For the function in `default_factory` we pass `uuid.uuid4`, which is a function that generates a **new UUID version 4**.

/// tip

We don't call `uuid.uuid4()` ourselves in the code (we don't put the parenthesis). Instead, we pass the function itself, just `uuid.uuid4`, so that SQLModel can call it every time we create a new instance.

///

This means that the UUID will be generated in the Python code, **before sending the data to the database**.

{* ./docs_src/advanced/uuid/tutorial001_py310.py ln[1:10] hl[1,7] *}

Pydantic has support for <a href="https://docs.pydantic.dev/latest/api/standard_library_types/#uuid" class="external-link" target="_blank">`UUID` types</a>.

For the database, **SQLModel** internally uses <a href="https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid" class="external-link" target="_blank">SQLAlchemy's `Uuid` type</a>.

### Create a Record with a UUID

When creating a `Hero` record, the `id` field will be **automatically populated** with a new UUID because we set `default_factory=uuid.uuid4`.

As `uuid.uuid4` will be called when creating the model instance, even before sending it to the database, we can **access and use the ID right away**.

And that **same ID (a UUID)** will be saved in the database.

{* ./docs_src/advanced/uuid/tutorial001_py310.py ln[23:34] hl[25,27,29,34] *}

### Select a Hero

We can do the same operations we could do with other fields.

For example we can **select a hero by ID**:

{* ./docs_src/advanced/uuid/tutorial001_py310.py ln[37:54] hl[49] *}

/// tip

Even if a database like SQLite stores the UUID as a string, we can select and run comparisons using a Python UUID object and it will work.

SQLModel (actually SQLAlchemy) will take care of making it work. ✨

///

#### Select with `session.get()`

We could also select by ID with `session.get()`:

{* ./docs_src/advanced/uuid/tutorial002_py310.py ln[37:53] hl[49] *}

The same way as with other fields, we could update, delete, etc. 🚀

### Run the program

If you run the program, you will see the **UUID** generated in the Python code, and then the record **saved in the database with the same UUID**.

<div class="termy">

```console
$ python app.py

// Some boilerplate and previous output omitted 😉

// In SQLite, the UUID will be stored as a string
// other DBs like Postgres have a specific UUID type
CREATE TABLE hero (
        id CHAR(32) NOT NULL,
        name VARCHAR NOT NULL,
        secret_name VARCHAR NOT NULL,
        age INTEGER,
        PRIMARY KEY (id)
)

// Before saving in the DB we already have the UUID
The hero before saving in the DB
name='Deadpond' secret_name='Dive Wilson' id=UUID('0e44c1a6-88d3-4a35-8b8a-307faa2def28') age=None
The hero ID was already set
0e44c1a6-88d3-4a35-8b8a-307faa2def28

// The SQL statement to insert the record uses our UUID
INSERT INTO hero (id, name, secret_name, age) VALUES (?, ?, ?, ?)
('0e44c1a688d34a358b8a307faa2def28', 'Deadpond', 'Dive Wilson', None)

// And indeed, the record was saved with the UUID we created 😎
After saving in the DB
age=None id=UUID('0e44c1a6-88d3-4a35-8b8a-307faa2def28') name='Deadpond' secret_name='Dive Wilson'

// Now we create a new hero (to select it in a bit)
Created hero:
age=None id=UUID('9d90d186-85db-4eaa-891a-def7b4ae2dab') name='Spider-Boy' secret_name='Pedro Parqueador'
Created hero ID:
9d90d186-85db-4eaa-891a-def7b4ae2dab

// And now we select it
Selected hero:
age=None id=UUID('9d90d186-85db-4eaa-891a-def7b4ae2dab') name='Spider-Boy' secret_name='Pedro Parqueador'
Selected hero ID:
9d90d186-85db-4eaa-891a-def7b4ae2dab
```

</div>

## Learn More

You can learn more about **UUIDs** in:

* The official <a href="https://docs.python.org/3/library/uuid.html" class="external-link" target="_blank">Python docs for UUID</a>.
* The <a href="https://en.wikipedia.org/wiki/Universally_unique_identifier" class="external-link" target="_blank">Wikipedia for UUID</a>.
