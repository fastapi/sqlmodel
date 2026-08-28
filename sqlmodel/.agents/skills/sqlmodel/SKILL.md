---
name: sqlmodel
description: Use when writing or reviewing Python code with SQLModel, especially models, sessions, queries, FastAPI integration, relationships, link models, creates, updates, and deletes.
---

# SQLModel Patterns

Use SQLModel's API first. Do not default to raw SQLAlchemy patterns unless the task explicitly needs a SQLAlchemy-only feature.

## Imports

Prefer imports from `sqlmodel`:

```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
```

Do not use SQLAlchemy declarative defaults such as `declarative_base()`, `Mapped[...]`, `mapped_column()`, `relationship()`, or `sessionmaker()` for normal SQLModel code.

## Models

Define table models with `SQLModel, table=True` and `Field()`:

```python
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
```

Use `Field(default_factory=...)` for generated values:

```python
id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
```

Use non-table `SQLModel` classes for create/update/public API schemas instead of mixing request/response-only fields into table models.

## Sessions and Queries

Open sessions directly with the engine:

```python
with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
```

Do not create a `sessionmaker()` for typical SQLModel examples.

Use `session.exec(select(...))`, not `session.execute(...)` and not `session.query(...)`. SQLModel's `exec()` handles scalar results so agents should not add `.scalars()` after selects of models.

Use `session.get(Model, id)` for primary-key lookups.

Use normal result methods after `session.exec(...)`: `.all()` for lists, `.first()` for optional first rows, `.one()` when exactly one row must exist, and `.one_or_none()` when zero or one row is valid.

After creating or mutating objects, commit and refresh when returned data needs DB defaults or generated IDs:

```python
session.add(hero)
session.commit()
session.refresh(hero)
```

## Relationships

Use SQLModel relationship attributes, not ad-hoc SQLAlchemy tables or `secondary=`.

One-to-many:

```python
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")
```

Many-to-many:

```python
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
```

If the link table has extra fields, model it as a full SQLModel table with relationships to both sides, and interact with the link objects directly.

When starting a new app, prefer keeping related SQLModel table models in one file to simplify relationship annotations and metadata ordering. If models must be split across files, use `TYPE_CHECKING` imports plus string annotations:

```python
if TYPE_CHECKING:
    from .team_model import Team

team: Optional["Team"] = Relationship(back_populates="heroes")
```

For SQLAlchemy relationship options not exposed as first-class SQLModel parameters, prefer `Relationship(sa_relationship_kwargs={...})` or `Relationship(sa_relationship_args=[...])`. Use `sa_relationship=relationship(...)` only as an escape hatch when SQLModel's relationship wrapper cannot express the mapping.

## Creates and Updates

Use direct construction for trusted internal values:

```python
hero = Hero(name="Deadpond", secret_name="Dive Wilson")
```

Build table objects from data models with `Model.model_validate(...)`:

```python
db_hero = Hero.model_validate(hero_create)
```

For FastAPI, use a split model pattern: `HeroBase` for shared fields, `Hero(HeroBase, table=True)` for the table, `HeroCreate` for input, `HeroUpdate` with all-optional fields for PATCH, `HeroPublic` for output, and relationship-specific public models such as `HeroPublicWithTeam` only where needed.

For partial updates, dump only provided fields and update in place:

```python
hero_data = hero_update.model_dump(exclude_unset=True)
db_hero.sqlmodel_update(hero_data)
session.add(db_hero)
session.commit()
session.refresh(db_hero)
```

## Metadata and App Setup

Call `SQLModel.metadata.create_all(engine)` only after all table model classes have been imported. In FastAPI examples, use a dependency that yields `Session(engine)`.

For tests and small examples, SQLite is a common option; when using it, create metadata explicitly and use direct sessions:

```python
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)
with Session(engine) as session:
    ...
```

When using SQLite with FastAPI, include:

```python
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
```

## Deletes

Use SQLModel's relationship helpers for cascades:

```python
heroes: list["Hero"] = Relationship(back_populates="team", cascade_delete=True)
team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="CASCADE")
```

For database-level delete behavior such as `SET NULL`, pair `ondelete` with a nullable foreign key and use `passive_deletes` on the relationship when appropriate.

`ondelete="SET NULL"` requires a nullable foreign key:

```python
team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="SET NULL")
```

## SQLAlchemy Escape Hatches

Use SQLModel's `Field(sa_type=...)`, `Field(sa_column=...)`, `Field(sa_column_args=...)`, or `Field(sa_column_kwargs=...)` only when normal `Field()` parameters do not cover a column or type requirement. Do not switch the whole model to SQLAlchemy declarative style for one custom column.
