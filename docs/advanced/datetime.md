# Datetimes and Timezones

You can use Python's `datetime` type to store dates and times, for example when a record was created.

A datetime can also contain **timezone information**:

* An **aware datetime** has timezone information. For example, `datetime.now(UTC)` creates an aware datetime in **UTC**.
* A **naive datetime** has no timezone information. On its own, it doesn't tell us which timezone the time belongs to.

/// note

The default UTC datetime behavior described here is available since SQLModel version `0.0.45`.

In version `0.0.44` and earlier, `datetime` fields used `DateTime(timezone=False)` by default. See [Upgrade Existing Applications](#upgrade-existing-applications) when upgrading.

///

## Models with Datetimes

Let's say that each event in our application has a `created_at` field.

We can declare it with `datetime` and use `default_factory` to generate the current time in UTC:

{* ./docs_src/advanced/datetime/tutorial001_py311.py ln[1:8] hl[1,8] *}

/// tip

The [`UTC` constant](https://docs.python.org/3/library/datetime.html#datetime.UTC) is available on Python 3.11 and newer. It is an alias for `timezone.utc`.

For Python 3.10, expand **Other versions and variants** below the example. That version imports `timezone` and uses `datetime.now(timezone.utc)` instead.

///

Here, `lambda` creates a small **function without a name**. It takes no arguments and returns `datetime.now(UTC)` when called.

We pass this function to `default_factory` so SQLModel can call it each time we create an `Event` without providing `created_at`. This way, each event gets its own creation time.

Passing `datetime.now(UTC)` directly would call it immediately, when defining the model class. `default_factory` needs a **function** to call later, not a datetime value.

We can create an event without passing a value for `created_at`:

{* ./docs_src/advanced/datetime/tutorial001_py311.py ln[17:19] hl[18] *}

For the database column, **SQLModel** uses `UTCDateTime`, a custom SQLAlchemy type based on `DateTime(timezone=True)`. It uses native timezone support when the database provides it.

### Write and Read Datetimes

Let's save the event to `database.db` and read it back using SQLite:

{* ./docs_src/advanced/datetime/tutorial001_py311.py ln[11:14,21:26] hl[23:25] *}

The datetime goes through these steps:

1. When we create the event, the default factory returns an **aware UTC datetime**.
2. When SQLModel sends the value to the database, `UTCDateTime` converts it to UTC. If it is already in UTC, the time stays the same.
3. When SQLModel reads the value back, `UTCDateTime` returns an **aware UTC datetime**, including when the database stores datetimes without timezone information.

For example, a value of `14:00+02:00` would come back as `12:00+00:00`. Both represent the same instant. The original timezone name or offset is not preserved.

This processing happens when executing database statements and reading their results. It doesn't change values when constructing a model or assigning attributes. The original value on an existing instance stays unchanged until it is refreshed or reloaded.

## Aware and Naive Datetimes

Pydantic provides [`AwareDatetime` and `NaiveDatetime`](https://docs.pydantic.dev/latest/api/standard_library_types/#datetimes) to validate whether a datetime has timezone information.

We can use them as field types:

{* ./docs_src/advanced/datetime/tutorial002_py310.py ln[1:8] hl[1,7:8] *}

Here, `starts_at` requires timezone information during validation. It uses the same database type as `datetime`: `UTCDateTime`.

The field `local_time` must have **no timezone information**. It uses `DateTime(timezone=False)`, for values that intentionally represent a local time without a timezone.

These types also work with `| None` and with `Annotated`, for example `Annotated[datetime, NaiveDatetime]`.

### Validate the Data

We can use `Event.model_validate()` to validate the data before creating an event:

{* ./docs_src/advanced/datetime/tutorial002_py310.py ln[11:17] hl[13:14,16] *}

The `Z` at the end of `starts_at` means **UTC**. The value for `local_time` has no timezone, so both values pass validation.

If we pass a naive value for `starts_at`, or an aware value for `local_time`, Pydantic raises a validation error.

/// note

For table models, constructing an instance directly with `Event(...)` currently does not enforce these Pydantic constraints. This will change in a future version of SQLModel. For now, use `Event.model_validate(data)` when you need validation.

Loading an instance from the database does not enforce these Pydantic constraints either.

///

Plain `datetime` still accepts both aware and naive values during **Pydantic validation**. But `UTCDateTime` rejects naive database parameters. It doesn't assume that a naive input means UTC or the computer's local timezone.

For example, using `datetime.now()` without a timezone would fail when the session flushes, including during `session.commit()`. SQLAlchemy raises a `StatementError` wrapping a `ValueError` that explains how to supply an aware datetime or use `NaiveDatetime`.

The same rule applies to datetime parameters in updates and queries, such as comparing a field to a datetime. Nullable fields still accept `None`.

Explicit `Field(sa_type=...)` and `Field(sa_column=...)` declarations continue to take precedence over the inferred database type. They bypass SQLModel's UTC processing unless they explicitly use `UTCDateTime`, which you can import from `sqlmodel`.

## Database Support

The underlying storage depends on the [SQLAlchemy dialect and database type](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime). `UTCDateTime` adds UTC processing around that storage:

* **PostgreSQL** uses `TIMESTAMP WITH TIME ZONE`. It stores an instant in time and returns it using the session timezone, without retaining the original timezone name or offset. `UTCDateTime` converts returned values to UTC.
* **SQLite** stores values without timezone information when using SQLAlchemy's default datetime format. `UTCDateTime` first converts the input to UTC, then restores UTC on the naive value read from the database.
* **MySQL and MariaDB** use `DATETIME`, which ignores the `timezone` flag. `UTCDateTime` supplies UTC values and restores UTC on naive results. It does not switch the column to MySQL's `TIMESTAMP` type.

You can read more in the [PostgreSQL datetime documentation](https://www.postgresql.org/docs/current/datatype-datetime.html), [SQLAlchemy SQLite documentation](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.DATETIME), and [SQLAlchemy MySQL documentation](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.DATETIME).

### Use UTC Datetimes

For timestamps that represent an instant in time, it is recommended using **UTC datetimes in your application code**, whichever database you use. Create them with `datetime.now(UTC)`, as in the [example above](#models-with-datetimes).

Raw SQL, other applications, and defaults generated by the database bypass the custom type's processing of input values. Make sure they also write UTC to columns that store datetimes without timezone information. For example, MySQL's `CURRENT_TIMESTAMP` uses the connection's timezone, so a connection generating these values needs to use UTC.

## Upgrade Existing Applications

/// warning

Changing the default from `DateTime(timezone=False)` to `UTCDateTime` is a **breaking change**. The new default requires aware database parameters and returns aware UTC values when reading.

Upgrading SQLModel changes your model metadata. It does **not** alter existing database columns or convert existing data. `SQLModel.metadata.create_all()` does not update existing columns either.

///

Review each datetime field and choose whether to keep naive storage or adopt UTC storage. Existing explicit `sa_type` or `sa_column` overrides retain their behavior, including an explicit `DateTime(timezone=True)`.

If you adopt UTC storage, keep `datetime` or use `AwareDatetime` to require aware input during validation. Follow the [UTC recommendation above](#use-utc-datetimes) for new timestamps. Update comparisons and query parameters to use aware values, and check API responses for the added UTC timezone information.

Before adopting UTC storage, determine what timezone existing naive values represent. This information cannot be recovered from the column type. Reading an old local time as UTC would change its meaning. Resolve ambiguous or nonexistent times around daylight-saving transitions and mixed or unknown timezones before converting data.

Back up the database and test schema changes, data conversions, and application behavior against a copy, using the same driver as production. Coordinate the migration with all writers so that old and new applications don't mix timezone conventions.

### Keep Naive Storage

Change the field annotation to `NaiveDatetime`:

{* ./docs_src/advanced/datetime/tutorial005_py310.py ln[1:9] hl[3,9] *}

This keeps the previous database column type, so no database migration is needed for that field. It also adds the validation constraint described above.

To retain the previous database type **and** plain `datetime` validation behavior, declare the database type explicitly:

{* ./docs_src/advanced/datetime/tutorial003_py310.py ln[1:9] hl[3,9] *}

### Adopt Timezone-Aware Storage on PostgreSQL

1. Create an Alembic migration with your models imported in `env.py` and `target_metadata=SQLModel.metadata`. Run `alembic revision --autogenerate -m "Use timezone-aware datetimes"`.
2. Review the generated migration. For each affected column, add an explicit conversion using the timezone of the existing values. Autogeneration cannot determine this timezone for you.
3. After testing, apply the migration with `alembic upgrade head` as part of the application deployment.

For example, if `event.created_at` contains naive **UTC** values, the operations in the generated revision can be:

{* ./docs_src/advanced/datetime/tutorial004_py310.py hl[9:11,19:21] *}

This migration uses `sa.DateTime(timezone=True)`, the underlying database type of `UTCDateTime`.

By default, Alembic renders this type as `sqlmodel.sql.sqltypes.UTCDateTime()`. Add `import sqlmodel.sql.sqltypes` at the top of the migration to use the generated code.

If the existing values represent another timezone, replace `UTC` in both `upgrade()` and `downgrade()` with that timezone. The downgrade converts instants back to naive values in the original timezone.

Without an explicit conversion, PostgreSQL interprets the old values using the database session's `TimeZone`, which can change the intended instants. Review server defaults and dependent indexes or constraints as part of the migration, too.

See [Alembic autogeneration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) and [`alter_column()`'s `postgresql_using` option](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.alter_column).

### Adopt UTC Storage on MySQL, MariaDB, and SQLite

These databases keep the same `DATETIME` column definition, so adopting `UTCDateTime` does **not** require a schema change by itself.

If existing values are already naive **UTC**, no data conversion is needed.

If they represent another timezone, create a **data migration** that converts them to UTC before the new application reads them.

Alembic's schema autogeneration cannot detect or generate this data conversion. An empty autogenerated migration does not mean the existing timestamps are ready for the new type.

### Other Databases

For other databases, inspect the generated column type and test writes and reads with the driver you use. Follow that database's schema and data migration procedures. Native timezone support and accepted input values vary by dialect and driver. Some require an explicit dialect-specific timestamp type.
