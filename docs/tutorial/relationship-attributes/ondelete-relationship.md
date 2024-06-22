## Foreign Key And Relationship Options: `ondelete`, `cascade`, and `passive_deletes`

### Overview

When working with relational databases, managing the deletion behavior of related records is crucial to maintaining data integrity. SQLModel provides robust support for handling these scenarios through the `ondelete`, `cascade`, and `passive_deletes` options. This guide will walk you through the usage and benefits of these features.

### First, let's declare our models and create some teams with their heroes


//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py[ln:1-73]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py[ln:99-101]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py[ln:106-107]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py[ln:1-77]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py[ln:103-105]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py[ln:110-111]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py[ln:1-77]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py[ln:103-105]!}


{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py[ln:110-111]!}

# Code below omitted 👇
```


////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py!}
```

////

///

### At this point we should have the next schema and data

#### Team table

| id   | name       | headquarters          |
| ---- | ---------- | --------------------- |
| 1    | Z-Force    | Sister Margaret's Bar |
| 2    | Preventers | Sharp Tower           |
| 3    | Wakaland   | Wakaland Capital City |

#### Hero Table

| id   | name            | secret_name      | age  | team_id |
| ---- | --------------- | ---------------- | ---- | ------- |
| 1    | Deadpond        | Dive WIlson      |      | 1       |
| 2    | Rusty-Man       | Tommy Sharp      | 48   | 2       |
| 3    | Spider-Boy      | Pedro Parqueador |      | 2       |
| 4    | Black Lion      | Trevor Challa    | 35   | 3       |
| 5    | Princess Sure-E | Sure-E           |      | 3       |



### `ondelete`

The `ondelete` option allows you to specify what should happen to dependent records when the referenced record is deleted. This is especially useful for managing foreign key constraints.

#### Supported Values

- `CASCADE`: Automatically deletes the dependent records.
- `SET NULL`: Sets the foreign key field to `NULL`.
- `RESTRICT`: Prevents the deletion if there are dependent records.

#### CASCADE Example

//// tab | Python 3.10+

```Python hl_lines="9 18"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11 21"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py[ln:1-23]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11 21"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py[ln:1-23]!}

# Code below omitted 👇
```


////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py!}
```

////

///

The configuration above is setting the table `Team` with a relationship with the flag `cascade_delete=True`, which means all objects in memory from the parent will be marked for delete. We are also setting `Hero` table in `team_id` column as a foreign key with the clause `ON DELETE CASCADE` at the database level, which means the database will delete any record when its parent in `Team` is deleted.

/// tip

The `ON DELETE CASCADE` setup at the database level is useful because if any other application or service has access to the database and delete a record, the database will be in charge to handle the situation to delete any possible child.

///

#### Removing a team with CASCADE

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py[ln:76-83]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py[ln:80-87]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py[ln:80-87]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial001.py!}
```

////

///

Removing the `Team` with the name `Wakaland` will leave our database like this.

##### Team table

| id   | name       | headquarters          |
| ---- | ---------- | --------------------- |
| 1    | Z-Force    | Sister Margaret's Bar |
| 2    | Preventers | Sharp Tower           |

##### Hero Table

| id   | name            | secret_name      | age  | team_id |
| ---- | --------------- | ---------------- | ---- | ------- |
| 1    | Deadpond        | Dive WIlson      |      | 1       |
| 2    | Rusty-Man       | Tommy Sharp      | 48   | 2       |
| 3    | Spider-Boy      | Pedro Parqueador |      | 2       |

The team was deleted and all of its heroes! 🤓

#### SET NULL Example

//// tab | Python 3.10+

```Python hl_lines="19"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py310.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="21"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py39.py[ln:1-23]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="21"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002.py[ln:1-23]!}

# Code below omitted 👇
```


////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002.py!}
```

////

///

The configuration above is setting `team_id` column from `Hero` table to `ON DELETE SET NULL` in all the child that belongs to the deleted parent.

/// tip

The foreign key should allow null values `nullable=True`, otherwise you are going to ended up in an Integrity Error by violating the not null constraint

///

#### Removing a team with SET NULL

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py310.py[ln:78-85]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py39.py[ln:80-87]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002.py[ln:80-87]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial002.py!}
```

////

///

The result will be.

##### Team table

| id   | name       | headquarters          |
| ---- | ---------- | --------------------- |
| 1    | Z-Force    | Sister Margaret's Bar |
| 2    | Preventers | Sharp Tower           |

##### Hero Table

| id   | name            | secret_name      | age  | team_id |
| ---- | --------------- | ---------------- | ---- | ------- |
| 1    | Deadpond        | Dive WIlson      |      | 1       |
| 2    | Rusty-Man       | Tommy Sharp      | 48   | 2       |
| 3    | Spider-Boy      | Pedro Parqueador |      | 2       |
| 4    | Black Lion      | Trevor Challa    | 35   | NULL    |
| 5    | Princess Sure-E | Sure-E           |      | NULL    |

The team `Wakaland` was deleted and all of its heroes were left without a team, which means with `team_id` NULL, but still kept in the database! 🤓

#### RESTRICT Example

//// tab | Python 3.10+

```Python hl_lines="10 19"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py310.py[ln:1-20]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="12 22"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py39.py[ln:1-24]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="12 22"
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003.py[ln:1-24]!}

# Code below omitted 👇
```


////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003.py!}
```

////

///

The configuration above is setting `team_id` column from `Hero` table to `ON DELETE RESTRICT`, which means if a parent has a dependant child, the database is going to check this before to proceed with any other task/transaction.

/// tip

* The default behavior of SQLAlchemy before to delete any object with a relationship in the database, it's disassociate them changing their relationship to set `NULL`. In this case since we are using the `RESTRICT` option we don't want that behavior, passing the argument `passive_deletes="all"` SQLAlchemy will not load the child objects to emit the delete, relying on the database to handle the constraint.

* The only difference of using `RESTRICT` instead on relying in the database Integrity Error here when we try to delete a parent record that has child, It's `RESTRICT` first, validate if there are existing records dependant on each other before to proceed with any delete and raise the error immediately, whereas the default behavior of the database is to execute the transactions and raise the error at the end of it.

///

#### Removing a team with RESTRICT

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py310.py[ln:81-88]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py39.py[ln:83-90]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003.py[ln:83-90]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/delete_records_relationship/tutorial003.py!}
```

////

///

The result will be the next error.

```bash
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) FOREIGN KEY constraint failed
[SQL: DELETE FROM team WHERE team.id = ?]
[parameters: (3,)]
```

So, the database prevents the delete and all of our records are still there. 🤓


### Summary

These options provide fine-grained control over the deletion behavior of related records in your database, helping to maintain data integrity and optimize performance. By leveraging `ondelete`, `cascade`, and `passive_deletes`, you can ensure that your application handles related records in a consistent and efficient manner.
