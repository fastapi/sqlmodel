# Define Relationships Attributes

Now we are finally in one of the most exciting parts of **SQLModel**.

Relationship Attributes. ✨

We currently have a `team` table:

<table>
<tr>
<th>id</th><th>name</th><th>headquarters</th>
</tr>
<tr>
<td>1</td><td>Preventers</td><td>Sharp Tower</td>
</tr>
<tr>
<td>2</td><td>Z-Force</td><td>Sister Margaret's Bar</td>
</tr>
</table>

And a `hero` table:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>2</td>
</tr>
<tr>
<td>2</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>1</td>
</tr>
<tr>
<td>3</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1</td>
</tr>
</table>

Now that you know how these tables work underneath and how the model classes represent them, it's time to add a little convenience that will make many operations in code simpler.

## Declare Relationship Attributes

Up to now, we have only used the `team_id` column to connect the tables when querying with `select()`:

//// tab | Python 3.10+

```Python hl_lines="16"
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py[ln:1-16]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="18"
{!./docs_src/tutorial/connect/insert/tutorial001.py[ln:1-18]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/connect/insert/tutorial001.py!}
```

////

///

This is a **plain field** like all the others, all representing a **column in the table**.

But now let's add a couple of new special attributes to these model classes, let's add `Relationship` attributes.

First, import `Relationship` from `sqlmodel`:

//// tab | Python 3.10+

```Python hl_lines="1"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py[ln:1]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py[ln:1-3]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py[ln:1-3]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py!}
```

////

///

Next, use that `Relationship` to declare a new attribute in the model classes:

//// tab | Python 3.10+

```Python hl_lines="9  19"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py[ln:1-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/define_relationship_attributes/tutorial001.py!}
```

////

///

## What Are These Relationship Attributes

These new attributes are not the same as fields, they **don't represent a column** directly in the database, and their value is not a singular value like an integer. Their value is the actual **entire object** that is related.

So, in the case of a `Hero` instance, if you call `hero.team`, you will get the entire `Team` instance object that this hero belongs to. ✨

For example, you could check if a `hero` belongs to any `team` (if `.team` is not `None`) and then print the team's `name`:

```Python
if hero.team:
    print(hero.team.name)
```

## Optional Relationship Attributes

Notice that in the `Hero` class, the type annotation for `team` is `Optional[Team]`.

This means that this attribute could be `None`, or it could be a full `Team` object.

This is because the related **`team_id` could also be `None`** (or `NULL` in the database).

If it was required for a `Hero` instance to belong to a `Team`, then the `team_id` would be `int` instead of `Optional[int]`, its `Field` would be `Field(foreign_key="team.id")` instead of `Field(default=None, foreign_key="team.id")` and the `team` attribute would be a `Team` instead of `Optional[Team]`.

## Relationship Attributes With Lists

And in the `Team` class, the `heroes` attribute is annotated as a list of `Hero` objects, because that's what it will have.

**SQLModel** (actually SQLAlchemy) is smart enough to know that the relationship is established by the `team_id`, as that's the foreign key that points from the `hero` table to the `team` table, so we don't have to specify that explicitly here.

/// tip

There's a couple of things we'll check again in some of the next chapters, about the `List["Hero"]` and the `back_populates`.

But for now, let's first see how to use these relationship attributes.

///

## Next Steps

Now let's see some real examples of how to use these new **relationship attributes** in the next chapters. ✨
