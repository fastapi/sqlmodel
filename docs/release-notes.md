# Release Notes

## Latest Changes

* ⬆ Upgrade mypy, fix type annotations. PR [#218](https://github.com/tiangolo/sqlmodel/pull/218) by [@tiangolo](https://github.com/tiangolo).

## 0.0.6

### Breaking Changes

**SQLModel** no longer creates indexes by default for every column, indexes are now opt-in. You can read more about it in PR [#205](https://github.com/tiangolo/sqlmodel/pull/205).

Before this change, if you had a model like this:

```Python
from typing import Optional

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

...when creating the tables, SQLModel version `0.0.5` and below, would also create an index for `name`, one for `secret_name`, and one for `age` (`id` is the primary key, so it doesn't need an additional index).

If you depended on having an index for each one of those columns, now you can (and would have to) define them explicitly:

```Python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
```

There's a high chance you don't need indexes for all the columns. For example, you might only need indexes for `name` and `age`, but not for `secret_name`. In that case, you could define the model as:

```Python
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
```

If you already created your database tables with SQLModel using versions `0.0.5` or below, it would have also created those indexes in the database. In that case, you might want to manually drop (remove) some of those indexes, if they are unnecessary, to avoid the extra cost in performance and space.

Depending on the database you are using, there will be a different way to find the available indexes.

For example, let's say you no longer need the index for `secret_name`. You could check the current indexes in the database and find the one for `secret_name`, it could be named `ix_hero_secret_name`. Then you can remove it with SQL:

```SQL
DROP INDEX ix_hero_secret_name
```

or

```SQL
DROP INDEX ix_hero_secret_name ON hero;
```

Here's the new, extensive documentation explaining indexes and how to use them: [Indexes - Optimize Queries](https://sqlmodel.tiangolo.com/tutorial/indexes/).

### Docs

* ✨ Document indexes and make them opt-in. Here's the new documentation: [Indexes - Optimize Queries](https://sqlmodel.tiangolo.com/tutorial/indexes/). This is the same change described above in **Breaking Changes**. PR [#205](https://github.com/tiangolo/sqlmodel/pull/205) by [@tiangolo](https://github.com/tiangolo).
* ✏ Fix typo in FastAPI tutorial. PR [#192](https://github.com/tiangolo/sqlmodel/pull/192) by [@yaquelinehoyos](https://github.com/yaquelinehoyos).
* 📝 Add links to the license file. PR [#29](https://github.com/tiangolo/sqlmodel/pull/29) by [@sobolevn](https://github.com/sobolevn).
* ✏ Fix typos in docs titles. PR [#28](https://github.com/tiangolo/sqlmodel/pull/28) by [@Batalex](https://github.com/Batalex).
* ✏ Fix multiple typos and some rewording. PR [#22](https://github.com/tiangolo/sqlmodel/pull/22) by [@egrim](https://github.com/egrim).
* ✏ Fix typo in `docs/tutorial/automatic-id-none-refresh.md`. PR [#14](https://github.com/tiangolo/sqlmodel/pull/14) by [@leynier](https://github.com/leynier).
* ✏ Fix typos in `docs/tutorial/index.md` and `docs/databases.md`. PR [#5](https://github.com/tiangolo/sqlmodel/pull/5) by [@sebastianmarines](https://github.com/sebastianmarines).

## 0.0.5

### Features

* ✨ Add support for Decimal fields from Pydantic and SQLAlchemy. Original PR [#103](https://github.com/tiangolo/sqlmodel/pull/103) by [@robcxyz](https://github.com/robcxyz). New docs: [Advanced User Guide - Decimal Numbers](https://sqlmodel.tiangolo.com/advanced/decimal/).

### Docs

* ✏ Update decimal tutorial source for consistency. PR [#188](https://github.com/tiangolo/sqlmodel/pull/188) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Split MkDocs insiders build in CI to support building from PRs. PR [#186](https://github.com/tiangolo/sqlmodel/pull/186) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Format `expression.py` and expression template, currently needed by CI. PR [#187](https://github.com/tiangolo/sqlmodel/pull/187) by [@tiangolo](https://github.com/tiangolo).
* 🐛Fix docs light/dark theme switcher. PR [#1](https://github.com/tiangolo/sqlmodel/pull/1) by [@Lehoczky](https://github.com/Lehoczky).
* 🔧 Add MkDocs Material social cards. PR [#90](https://github.com/tiangolo/sqlmodel/pull/90) by [@tiangolo](https://github.com/tiangolo).
* ✨ Update type annotations and upgrade mypy. PR [#173](https://github.com/tiangolo/sqlmodel/pull/173) by [@tiangolo](https://github.com/tiangolo).

## 0.0.4

* 🎨 Fix type detection of select results in PyCharm. PR [#15](https://github.com/tiangolo/sqlmodel/pull/15) by [@tiangolo](https://github.com/tiangolo).

## 0.0.3

* ⬆️ Update and relax specification range for `sqlalchemy-stubs`. PR [#4](https://github.com/tiangolo/sqlmodel/pull/4) by [@tiangolo](https://github.com/tiangolo).

## 0.0.2

* This includes several small bug fixes detected during the first CI runs.
* 💚 Fix CI installs and tests. PR [#2](https://github.com/tiangolo/sqlmodel/pull/2) by [@tiangolo](https://github.com/tiangolo).

## 0.0.1

* First release. 🎉
