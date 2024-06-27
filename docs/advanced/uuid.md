# UUID (Universally Unique Identifier)

### Introduction

This guide demonstrates how to implement UUID (Universally Unique Identifier) support in SQLModel, providing a robust method for creating unique identifiers across your database tables. You can read more about UUID in the official <a href="https://docs.python.org/3/library/uuid.html" class="external-link" target="_blank">Python docs for UUID</a>.

### Prerequisites

Ensure you have the correct version of SQLModel:

- SQLModel 0.0.20+

### Adding UUID Support

#### Defining Models with UUID

Pydantic has support for <a href="https://docs.pydantic.dev/latest/api/standard_library_types/#uuid" class="external-link" target="_blank">`UUIDs` types</a>.

To use UUIDs as primary keys, you need to modify your model definitions to include `uuid.UUID` as the type for the ID field. Here's an example for an `Item` model.

/// info

For the database, **SQLModel** will use <a href="https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid" class="external-link" target="_blank">`sqlalchemy.sql.sqltypes.Uuid` type</a>.

///

#### Item Model with UUID

//// tab | Python 3.10+

```Python hl_lines="7"
{!./docs_src/advanced/uuid/tutorial001_py310.py[ln:1-9]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
{!./docs_src/advanced/uuid/tutorial001.py[ln:1-10]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/uuid/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/uuid/tutorial001.py!}
```

////

///

### Working with UUIDs

#### Creating Records with UUIDs

When creating an `Item` record, the `id` field will be automatically populated with a new UUID as `default_factory=uuid.uuid4` is set:

//// tab | Python 3.10+

```Python
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001_py310.py[ln:12-18]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001.py[ln:13-19]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/uuid/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/uuid/tutorial001.py!}
```

////

///

/// info

We are using here `uuid.uuid4` as they are safe, enough long and unique to use as a primary key

///

#### Querying Records by UUID

To query an `Item` by its UUID, use the following pattern:

//// tab | Python 3.10+

```Python hl_lines="3 5"
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001_py310.py[ln:21-24]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3 5"
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001.py[ln:22-25]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/uuid/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/uuid/tutorial001.py!}
```

////

///

#### Deleting Records by UUID

To delete an `Item` using its UUID:

//// tab | Python 3.10+

```Python hl_lines="3 5"
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001_py310.py[ln:27-32]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3 5"
# Code above omitted 👆

{!./docs_src/advanced/uuid/tutorial001.py[ln:28-33]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/uuid/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/uuid/tutorial001.py!}
```

////

///

### Example Usage

Here's a complete example demonstrating the creation, querying, and deletion of records with UUIDs:

//// tab | Python 3.10+

```Python hl_lines="39 41 45"
{!./docs_src/advanced/uuid/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python hl_lines="40 42 46"
{!./docs_src/advanced/uuid/tutorial001.py!}
```

////

### Conclusion

This guide provided a focused overview of implementing UUID support in SQLModel. By following these steps, you can ensure that your models have robust, unique identifiers, enhancing the reliability and scalability of your application.
