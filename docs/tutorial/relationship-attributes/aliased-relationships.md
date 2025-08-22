# Aliased Relationships

## Multiple Relationships to the Same Model

We've seen how tables are related to each other via a single relationship attribute but what if more than
one attribute links to the same table?

What if you have a `User` model and an `Address` model and would like
to have `User.home_address` and `User.work_address` relationships to the same
`Address` model? In SQL you do this by creating a table alias using `AS` like this:

```
SELECT *
FROM user
JOIN address AS home_address_alias
    ON user.home_address_id == home_address_alias.id
JOIN address AS work_address_alias
    ON user.work_address_id == work_address_alias.id
```

The aliases we create are `home_address_alias` and `work_address_alias`.  You can think of them
as a view to the same underlying `address` table.

We can do this with **SQLModel** and **SQLAlchemy** using `sqlalchemy.orm.aliased`
and a couple of extra bits of info in our **SQLModel** relationship definition and join statements.

## The Relationships

Let's define a `winter_team` and `summer_team` relationship for our heros.  They can be on different
winter and summer teams or on the same team for both seasons.

```Python hl_lines="11  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py[ln:13-26]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py!}
```

///

The `sa_relationship_kwargs={"primaryjoin": ...}` is a new bit of info we need for **SQLAlchemy** to
figure out which SQL join we should use depending on which attribute is in our query.

## Creating Heros

Creating `Heros` with the multiple teams is no different from before. We set the same or different
team to the `winter_team` and `summer_team` attributes:


```Python hl_lines="11-12 18-19"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py[ln:39-65]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py!}
```

///
## Searching for Heros

Querying `Heros` based on the winter or summer teams adds a bit of complication.  We need to create the
alias and we also need to be a bit more explicit in how we tell **SQLAlchemy** to join the `hero` and `team` tables.

We create the alias using `sqlalchemy.orm.aliased` function and use the alias in the `where` function.  We also
need to provide an `onclause` argument to the `join`.

```Python hl_lines="3 8 9"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py[ln:70-79]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py!}
```

///
The value for the `onclause` is the same value that you used in the `primaryjoin` argument
when the relationship is defined in the `Hero` model.

To use both team attributes in a query, create another `alias` and add the join:

```Python hl_lines="3 9 10"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py[ln:82-95]!}

# Code below omitted 👇
```
/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/aliased_relationship/tutorial001.py!}
```

///
