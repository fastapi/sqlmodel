# Column Types

In the tutorial, we stored scalar data types in our tables, like strings, numbers and timestamps. In practice, we often work with more complicated types that need to be converted to a data type our database supports.

## Customising String Field Lengths

As we discussed in [`TEXT` or `VARCHAR`](../tutorial/create-db-and-table.md#text-or-varchar), a `str` field type will be created as a `VARCHAR`, which has varying maximum-lengths depending on the database engine you are using.

For cases where you know you only need to store a certain length of text, string field maximum length can be reduced using the `max_length` validation argument to `Field()`:

```Python hl_lines="11"
{!./docs_src/advanced/column_types/tutorial001.py[ln:1-12]!}
```

/// details | 👀 Full file preview

```Python
{!./docs_src/advanced/column_types/tutorial001.py!}
```

///

/// warning

Database engines behave differently when you attempt to store longer text than the character length of the `VARCHAR` column. Notably:

* SQLite does not enforce the length of a `VARCHAR`. It will happily store up to 500-million characters of text.
* MySQL will emit a warning, but will also truncate your text to fit the size of the `VARCHAR`.
* PostgreSQL will respond with an error code, and your query will not be executed.

///

However if you need to store much longer strings than `VARCHAR` can allow, databases provide `TEXT` or `CLOB` (**c**haracter **l**arge **ob**ject) column types. We can use these by specifying an SQLAlchemy column type to the field with the `sa_type` keyword argument:

```Python hl_lines="12"
{!./docs_src/advanced/column_types/tutorial001.py[ln:5-45]!}
```

/// tip

`Text` also accepts a character length argument, which databases use to optimise the storage of a particular field. Some databases support `TINYTEXT`, `SMALLTEXT`, `MEDIUMTEXT` and `LONGTEXT` column types - ranging from 255 bytes to 4 gigabytes. If you know the maximum length of data, specifying it like `Text(1000)` will automatically select the best-suited, supported type for your database engine.

///


With this approach, we can use [any kind of SQLAlchemy type](https://docs.sqlalchemy.org/en/20/core/type_basics.html). For example, we can store pickled objects in the database:

```Python
{!./docs_src/advanced/column_types/tutorial002.py!}
```

## Supported Types

Python types are mapped to column types as so:

<table>
<tr>
<th>Python type</th><th>SQLAlchemy type</th><th>Database column types</th>
</tr>
<tr>
<td>str</td><td>String</td><td>VARCHAR</td>
</tr>
<tr>
<td>int</td><td>Integer</td><td>INTEGER</td>
</tr>
<tr>
<td>float</td><td>Float</td><td>FLOAT, REAL, DOUBLE</td>
</tr>
<tr>
<td>bool</td><td>Boolean</td><td>BOOL or TINYINT</td>
</tr>
<tr>
<td>datetime.datetime</td><td>DateTime</td><td>DATETIME, TIMESTAMP, DATE</td>
</tr>
<tr>
<td>datetime.date</td><td>Date</td><td>DATE</td>
</tr>
<tr>
<td>datetime.timedelta</td><td>Interval</td><td>INTERVAL, INT</td>
</tr>
<tr>
<td>datetime.time</td><td>Time</td><td>TIME, DATETIME</td>
</tr>
<tr>
<td>bytes</td><td>LargeBinary</td><td>BLOB, BYTEA</td>
</tr>
<tr>
<td>Decimal</td><td>Numeric</td><td>DECIMAL, FLOAT</td>
</tr>
<tr>
<td>enum.Enum</td><td>Enum</td><td>ENUM, VARCHAR</td>
</tr>
<tr>
<td>uuid.UUID</td><td>GUID</td><td>UUID, CHAR(32)</td>
</tr>
</table>

In addition, the following types are stored as `VARCHAR`:

* ipaddress.IPv4Address
* ipaddress.IPv4Network
* ipaddress.IPv6Address
* ipaddress.IPv6Network
* pathlib.Path
* pydantic.networks.IPvAnyAddress
* pydantic.networks.IPvAnyInterface
* pydantic.networks.IPvAnyNetwork
* pydantic.EmailStr

Note that while the column types for these are `VARCHAR`, values are not converted to and from strings.   

### IP Addresses

IP Addresses from the [Python `ipaddress` module](https://docs.python.org/3/library/ipaddress.html){.external-link target=_blank} are stored as text.

```Python hl_lines="5 11"
{!./docs_src/advanced/column_types/tutorial003.py[ln:1-15]!}
```

### Filesystem Paths

Paths to files and directories using the [Python `pathlib` module](https://docs.python.org/3/library/pathlib.html){.external-link target=_blank} are stored as text.

```Python hl_lines="2 12"
{!./docs_src/advanced/column_types/tutorial003.py[ln:1-15]!}
```

/// tip

The stored value of a Path is the basic string value: `str(Path('../path/to/file'))`. If you need to store the full path ensure you call `absolute()` on the path before setting it in your model.

///

### UUIDs

UUIDs from the [Python `uuid` module](https://docs.python.org/3/library/uuid.html){.external-link target=_blank} are stored as native `UUID` types in supported databases (just PostgreSQL at the moment), otherwise as a `CHAR(32)`.

```Python hl_lines="3 10"
{!./docs_src/advanced/column_types/tutorial003.py[ln:1-15]!}
```

### Email Addresses

Email addresses using [Pydantic's `EmailStr` type](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.EmailStr){.external-link target=_blank} are stored as strings.

```Python hl_lines="5 14"
{!./docs_src/advanced/column_types/tutorial003.py[ln:1-15]!}
```


## Custom Pydantic types

As SQLModel is built on Pydantic, you can use any custom type as long as it would work in a Pydantic model. However, if the type is not a subclass of [a type from the table above](#supported-types), you will need to specify an SQLAlchemy type to use.
