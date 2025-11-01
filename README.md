<p align="center">
  <a href="https://sqlmodel.tiangolo.com"><img src="https://sqlmodel.tiangolo.com/img/logo-margin/logo-margin-vector.svg#only-light" alt="SQLModel"></a>

</p>
<p align="center">
    <em>SQLModel with Protocol Buffers & gRPC support</em>
</p>
<p align="center">
    <em>A fork of SQLModel adding seamless protobuf/gRPC integration</em>
</p>

---

## 🚀 What is this?

This is a **fork of [SQLModel](https://github.com/fastapi/sqlmodel)** that extends the original library with **Protocol Buffers (protobuf) and gRPC integration**. SQLModel is a library for interacting with <abbr title='Also called "Relational databases"'>SQL databases</abbr> from Python code, with Python objects.

**Original SQLModel**: <a href="https://sqlmodel.tiangolo.com" target="_blank">https://sqlmodel.tiangolo.com</a> | <a href="https://github.com/fastapi/sqlmodel" target="_blank">GitHub</a>

---

SQLModel is a library for interacting with <abbr title='Also called "Relational databases"'>SQL databases</abbr> from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust.

**SQLModel** is based on Python type annotations, and powered by <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> and <a href="https://sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>.

The key features are:

* **Intuitive to write**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
* **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
* **Compatible**: It is designed to be compatible with **FastAPI**, Pydantic, and SQLAlchemy.
* **Extensible**: You have all the power of SQLAlchemy and Pydantic underneath.
* **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in SQLAlchemy and Pydantic.
* **🆕 Protocol Buffers Integration**: SQLModel classes now implement the protobuf `Message` interface, enabling direct serialization/deserialization and gRPC compatibility.
* **🆕 Automatic Descriptor Generation**: Protobuf descriptors are automatically synthesized from your SQLModel classes with intelligent type inference.
* **🆕 gRPC Ready**: Use your SQLModel models directly in gRPC services without additional conversion code.

## SQL Databases in FastAPI

<a href="https://fastapi.tiangolo.com" target="_blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" style="width: 20%;"></a>

**SQLModel** is designed to simplify interacting with SQL databases in <a href="https://fastapi.tiangolo.com" class="external-link" target="_blank">FastAPI</a> applications, it was created by the same <a href="https://tiangolo.com/" class="external-link" target="_blank">author</a>. 😁

It combines SQLAlchemy and Pydantic and tries to simplify the code you write as much as possible, allowing you to reduce the **code duplication to a minimum**, but while getting the **best developer experience** possible.

**SQLModel** is, in fact, a thin layer on top of **Pydantic** and **SQLAlchemy**, carefully designed to be compatible with both.

## New Features: Protocol Buffers & gRPC Integration

This fork extends SQLModel with seamless Protocol Buffers (protobuf) and gRPC support:

### ✨ Key Additions

1. **Protobuf Message Interface**: All SQLModel classes now inherit from `google.protobuf.message.Message`, making them fully compatible with protobuf serialization and gRPC.

2. **Automatic Descriptor Generation**: Protobuf descriptors are automatically synthesized from your SQLModel class definitions, with intelligent type inference from Python type annotations.

3. **Full Protobuf API**: All standard protobuf methods are implemented:
   - `SerializeToString()` / `serialize_to_string()` - Serialize to binary
   - `ParseFromString()` / `parse_from_string()` - Deserialize from binary
   - `MergeFrom()` / `merge_from()` - Merge from another message
   - `Clear()` / `clear()` - Reset to defaults
   - `HasField()` / `has_field()` - Check field presence
   - And more...

4. **Type Inference**: Automatically maps Python types to protobuf field types:
   - `int` → `TYPE_INT64`
   - `float` → `TYPE_DOUBLE`
   - `bool` → `TYPE_BOOL`
   - `str` → `TYPE_STRING`
   - `bytes` → `TYPE_BYTES`
   - Lists/tuples → `LABEL_REPEATED`

5. **Custom Field Descriptors**: Optionally provide custom protobuf field descriptors via `Field(grpc_descriptor=...)` for fine-grained control.

### Example: Using SQLModel with gRPC

```Python
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None = None

# Create a hero instance
hero = Hero(name="Deadpond", age=30)

# Serialize to protobuf binary format
serialized = hero.SerializeToString()

# Deserialize back
hero2 = Hero()
hero2.ParseFromString(serialized)

# Use directly in gRPC services!
# Your SQLModel classes work seamlessly with gRPC
```

## Requirements

A recent and currently supported <a href="https://www.python.org/downloads/" class="external-link" target="_blank">version of Python</a>.

As **SQLModel** is based on **Pydantic** and **SQLAlchemy**, it requires them. They will be automatically installed when you install SQLModel.

**Additional requirement for this fork**: `protobuf>=5.29.5` (automatically installed).

## Installation

Make sure you create a <a href="https://sqlmodel.tiangolo.com/virtual-environments/" class="external-link" target="_blank">virtual environment</a>, activate it, and then install this fork:

<div class="termy">

```console
# Install from source (this fork)
$ uv pip install -e .

# Or install directly from git
$ uv pip install git+https://github.com/YOUR_USERNAME/grpcmodel.git
```

</div>

**Note**: For the original SQLModel without protobuf support, install from PyPI:
```console
$ uv pip install sqlmodel
```

## Example

For an introduction to databases, SQL, and everything else, see the <a href="https://sqlmodel.tiangolo.com/databases/" target="_blank">SQLModel documentation</a>.

Here's a quick example. ✨

### A SQL Table

Imagine you have a SQL table called `hero` with:

* `id`
* `name`
* `secret_name`
* `age`

And you want it to have this data:

| id | name | secret_name | age |
-----|------|-------------|------|
| 1  | Deadpond | Dive Wilson | null |
| 2  | Spider-Boy | Pedro Parqueador | null |
| 3  | Rusty-Man | Tommy Sharp | 48 |

### Create a SQLModel Model

Then you could create a **SQLModel** model like this:

```Python
from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```

That class `Hero` is a **SQLModel** model, the equivalent of a SQL table in Python code.

And each of those class attributes is equivalent to each **table column**.

### Create Rows

Then you could **create each row** of the table as an **instance** of the model:

```Python
hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
```

This way, you can use conventional Python code with **classes** and **instances** that represent **tables** and **rows**, and that way communicate with the **SQL database**.

### Editor Support

Everything is designed for you to get the best developer experience possible, with the best editor support.

Including **autocompletion**:

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/autocompletion01.png">

And **inline errors**:

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/inline-errors01.png">

### Write to the Database

You can learn a lot more about **SQLModel** by quickly following the **tutorial**, but if you need a taste right now of how to put all that together and save to the database, you can do this:

```Python hl_lines="16  19  21-25"
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
```

That will save a **SQLite** database with the 3 heroes.

### Select from the Database

Then you could write queries to select from that same database, for example with:

```Python hl_lines="13-17"
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


engine = create_engine("sqlite:///database.db")

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)
```

### Editor Support Everywhere

**SQLModel** was carefully designed to give you the best developer experience and editor support, **even after selecting data** from the database:

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/autocompletion02.png">

## SQLAlchemy, Pydantic, and Protocol Buffers

That class `Hero` is a **SQLModel** model.

But at the same time, ✨ it is a **SQLAlchemy** model ✨. So, you can combine it and use it with other SQLAlchemy models, or you could easily migrate applications with SQLAlchemy to **SQLModel**.

And at the same time, ✨ it is also a **Pydantic** model ✨. You can use inheritance with it to define all your **data models** while avoiding code duplication. That makes it very easy to use with **FastAPI**.

**And now**, ✨ it is also a **protobuf Message** ✨. You can serialize it to binary format, use it directly in gRPC services, and interact with any protobuf-based system without additional conversion layers.

## Differences from Original SQLModel

This fork maintains 100% compatibility with the original SQLModel while adding:

- ✅ All original SQLModel features work exactly as before
- ✅ New protobuf/gRPC capabilities seamlessly integrated
- ✅ Automatic descriptor generation (no extra code needed)
- ✅ Backward compatible - existing code continues to work

## Contributing

This is a fork of the original SQLModel. For issues and contributions related to:
- **Core SQLModel features**: Please refer to the [original SQLModel repository](https://github.com/fastapi/sqlmodel)
- **Protobuf/gRPC features**: Please open issues in this repository

## License

This project is licensed under the terms of the [MIT license](LICENSE), same as the original SQLModel.
