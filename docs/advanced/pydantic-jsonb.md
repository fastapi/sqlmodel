# Storing Pydantic Models in JSONB Columns

You can store Pydantic models (and lists or dicts of them) in JSON or JSONB database columns using the `PydanticJSONB` utility.

This is especially useful when:

- You want to persist flexible, nested data structures in your models.
- You prefer to avoid separate relational tables for structured fields like metadata, config, or address.
- You want automatic serialization and deserialization using Pydantic.

## Usage

You can use it with SQLModel like this:

```python
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
from sqlmodel.sql.sqltypes import PydanticJSONB

class Address(BaseModel):
    street: str
    city: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: Address = Field(sa_column=Column(PydanticJSONB(Address)))
```

This will store the `address` field as a `JSONB` column in PostgreSQL and automatically serialize/deserialize to and from the `Address` Pydantic model.

If you're using a list or dict of models, `PydanticJSONB` supports that too:

```python
Field(sa_column=Column(PydanticJSONB(List[SomeModel])))
Field(sa_column=Column(PydanticJSONB(Dict[str, SomeModel])))
```

## Requirements

* PostgreSQL (for full `JSONB` support).
* Pydantic v2.
* SQLAlchemy 2.x.

## Limitations

### Nested Model Updates

Currently, updating attributes inside a nested Pydantic model doesn't automatically trigger a database update. This is similar to how plain dictionaries work in SQLAlchemy. For example:

```python
# This won't trigger a database update
row = select(...)  # some MyTable row
row.data.x = 1
db.add(row)  # no effect, change isn't detected
```

To update nested model attributes, you need to reassign the entire model:

```python
# Workaround: Create a new instance and reassign
updated = ExtraData(**row.data.model_dump())
updated.x = 1
row.data = updated
db.add(row)
```

This limitation will be addressed in a future update using `MutableDict` to enable change tracking for nested fields. The `MutableDict` implementation will emit change events when the contents of the dictionary are altered, including when values are added or removed.

## Notes

* Falls back to `JSON` if `JSONB` is not available.
* Only tested with PostgreSQL at the moment.
