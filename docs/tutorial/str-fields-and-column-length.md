# String fields and column length

Some databases have a limit on the length of string columns (e.g., `VARCHAR(255)` in *MySQL*) and fail with an error if you try to create a string column without specifying a length.

**SQLModel** handles this automatically depending on the database dialect you are using. 😎

For databases that require a length for string columns, **SQLModel** will automatically set a default length (e.g., `255` for *MySQL*) if you do not specify one.

{* ./docs_src/tutorial/str_fields_and_column_length/tutorial001_py310.py ln[4:6] hl[6] *}

If you run this code with *MySQL*, **SQLModel** will create the `name` column as `VARCHAR(255)`:

```sql
CREATE TABLE hero (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
)
```

But you can always override this by specifying a custom length if needed:

{* ./docs_src/tutorial/str_fields_and_column_length/tutorial002_py310.py ln[4:6] hl[6] *}

```sql
CREATE TABLE hero (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
)
```
This works thanks to `AutoString` type that **SQLModel** uses for all string fields by default.

But if you specify the database type of column explicitly, **SQLModel** will not be able to set the length automatically, and you will need to specify it manually:

{* ./docs_src/tutorial/str_fields_and_column_length/tutorial003_py310.py ln[1:6] hl[1,6] *}

The code example above will fail on databases that require a length for string columns:

```console
sqlalchemy.exc.CompileError: (in table 'hero', column 'name'): VARCHAR requires a length on dialect mysql
```

To fix it, you need to specify the length explicitly as follows:

{* ./docs_src/tutorial/str_fields_and_column_length/tutorial004_py310.py ln[1:6] hl[1,6] *}

This will give:

```sql
CREATE TABLE hero (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
)
```
