<p align="center">
  <a href="https://sqlmodel.tiangolo.com"><img src="https://sqlmodel.tiangolo.com/img/logo-margin/logo-margin-vector.svg" alt="SQLModel"></a>
</p>
<p align="center">
    <em>SQLModel, SQL databases in Python, designed for simplicity, compatibility, and robustness.</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/sqlmodel/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/sqlmodel/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/tiangolo/sqlmodel/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/sqlmodel/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://codecov.io/gh/tiangolo/sqlmodel" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/sqlmodel?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/sqlmodel" target="_blank">
    <img src="https://img.shields.io/pypi/v/sqlmodel?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://sqlmodel.tiangolo.com" target="_blank">https://sqlmodel.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/sqlmodel" target="_blank">https://github.com/tiangolo/sqlmodel</a>

---

SQLModel is a library for interacting with <abbr title='Also called "Relational databases"'>SQL databases</abbr> from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust.

**SQLModel** is based on Python type annotations, and powered by <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> and <a href="https://sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>.

The key features are:

* **Intuitive to write**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
* **Easy to use**: It has sensible defaults and does a lot of work underneath to simplify the code you write.
* **Compatible**: It is designed to be compatible with **FastAPI**, Pydantic, and SQLAlchemy.
* **Extensible**: You have all the power of SQLAlchemy and Pydantic underneath.
* **Short**: Minimize code duplication. A single type annotation does a lot of work. No need to duplicate models in SQLAlchemy and Pydantic.

## SQL Databases in FastAPI

<a href="https://fastapi.tiangolo.com" target="_blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" style="width: 20%;"></a>

**SQLModel** is designed to simplify interacting with SQL databases in <a href="https://fastapi.tiangolo.com" class="external-link" target="_blank">FastAPI</a> applications, it was created by the same <a href="https://tiangolo.com/" class="external-link" target="_blank">author</a>. 😁

It combines SQLAlchemy and Pydantic and tries to simplify the code you write as much as possible, allowing you to reduce the **code duplication to a minimum**, but while getting the **best developer experience** possible.

**SQLModel** is, in fact, a thin layer on top of **Pydantic** and **SQLAlchemy**, carefully designed to be compatible with both.

## Requirements

A recent and currently supported version of Python (right now, <a href="https://www.python.org/downloads/" class="external-link" target="_blank">Python supports versions 3.6 and above</a>).

As **SQLModel** is based on **Pydantic** and **SQLAlchemy**, it requires them. They will be automatically installed when you install SQLModel.

## Installation

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
Successfully installed sqlmodel
```

</div>

## Example

For an introduction to databases, SQL, and everything else, see the <a href="https://sqlmodel.tiangolo.com" target="_blank">SQLModel documentation</a>.

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
from typing import Optional

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
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

```Python hl_lines="18  21  23-27"
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


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

```Python hl_lines="15-18"
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


engine = create_engine("sqlite:///database.db")

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)
```

### Editor Support Everywhere

**SQLModel** was carefully designed to give you the best developer experience and editor support, **even after selecting data** from the database:

<img class="shadow" src="https://sqlmodel.tiangolo.com/img/index/autocompletion02.png">

## SQLAlchemy and Pydantic

That class `Hero` is a **SQLModel** model.

But at the same time, ✨ it is a **SQLAlchemy** model ✨. So, you can combine it and use it with other SQLAlchemy models, or you could easily migrate applications with SQLAlchemy to **SQLModel**.

And at the same time, ✨ it is also a **Pydantic** model ✨. You can use inheritance with it to define all your **data models** while avoiding code duplication. That makes it very easy to use with **FastAPI**.

## License

This project is licensed under the terms of the [MIT license](https://github.com/tiangolo/sqlmodel/blob/main/LICENSE).
