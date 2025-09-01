# Multiple Relationships to the Same Model

We've seen how tables are related to each other via a single relationship attribute but what if more than
one attribute links to the same table?

What if you have a `User` model and an `Address` model and would like
to have `User.home_address` and `User.work_address` relationships to the same
`Address` model? In SQL you do this one of two ways: 1) by creating a table alias using `AS` or 2)
by using a correlated sub-query.

Query: Find users with home address zipcode "100000" and work address zipcode = "10001":

### Alias Query

Using an alias, JOIN the address table twice:
```
SELECT *
FROM user
JOIN address AS home_address_alias
    ON user.home_address_id == home_address_alias.id
JOIN address AS work_address_alias
    ON user.work_address_id == work_address_alias.id
WHERE
    home_address_alias.zipcode == "10000"
    AND work_address_alias.zipcode == "10001"
```

### Correlated Sub-Query
Using sub-queries, filter the matches with EXISTS:
```
SELECT *
FROM user
WHERE (
    EXISTS (
    SELECT 1 FROM address
    WHERE
        address.id = user.home_address_id
        AND address.zipcode = "10000"
  )
) AND (
    EXISTS (
    SELECT 1 FROM address
    WHERE
        address.id = user.work_address_id
        AND address.zipcode = "10001"
  )

```

### Key differences

Duplicates: JOIN (alias query) can produce them, EXISTS will not. The duplicates will be removed by the ORM
as rows are marshalled into objects.

Performance: Both can be optimized similarly, but JOIN often wins when you’re retrieving columns from the related table.

Readability: JOIN reads like “combine these tables.” EXISTS reads like “filter by a condition.”

✅ Rule of thumb:

If you need columns from the foreign table → use JOIN. For example, if you are using `lazy=joined` or `selectin` you may prefer this.

If you only care whether a row exists in the foreign table → use EXISTS.

If the foreign table search criteria (address.zipcode) is not unique, prefer EXISTS unless you also want the duplicates.

## The Relationships

Let's define a `winter_team` and `summer_team` relationship for our heros.  They can be on different
winter and summer teams or on the same team for both seasons.

{* ./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001_py310.py ln[13:26] hl[9,13] *}

The `sa_relationship_kwargs={"foreign_keys": ...}` is a new bit of info we need for **SQLAlchemy** to
figure out which SQL join we should use depending on which attribute is in our query.

## Creating Heros

Creating `Heros` with the multiple teams is no different from before. We set the same or different
team to the `winter_team` and `summer_team` attributes:


```Python hl_lines="11-12 18-19"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py[ln:39-65]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py!}
```

///
## Searching for Heros

Querying `Heros` based on the winter or summer teams adds a bit of complication.  As
mentioned above, we can solve this with an aliased join or correlated subquery.

### Alias Join

To use the alias method we need to: 1) create the alias(es) and 2) provide the join in our query.

#### Aliases

We create the alias using `sqlalchemy.orm.aliased` function and use the alias in the `where` function.  We also
need to provide an `onclause` argument to the `join`.

The aliases we create are `home_address_alias` and `work_address_alias`.  You can think of them
as a view to the same underlying `address` table. We can do this with **SQLModel** and **SQLAlchemy** using `sqlalchemy.orm.aliased`
and a couple of extra bits of info in our **SQLModel** join statements.

```Python hl_lines="2"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py[ln:69-71]!}

# Code below omitted 👇
```

#### Join

Query Heros filtering by Team attributes by manually specifying the `join` with an `onclause` to tell **SQLAlchemy** to join the `hero` and `team` tables.

```Python hl_lines="7"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py[ln:69-89]!}

# Code below omitted 👇
```

The value for the `onclause` is the join using the same foreign key
when the relationship is defined in the `Hero` model.

To use both team attributes in a query, create another `alias` and add the join.

For more information see [SQLAlchemy: Handling Multiple Join Paths](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#handling-multiple-join-paths).

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py!}
```

///

#### Correlated Sub Query

From a query perspecitve, this is a much simpler solution.  We use the `has` function in the query:

```Python hl_lines="4 5"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py[ln:93-123]!}

# Code below omitted 👇
```
/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/relationship_attributes/multiple_relationships_same_model/tutorial001.py!}
```

///
