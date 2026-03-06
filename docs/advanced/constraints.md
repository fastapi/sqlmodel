# Database Constraints

Database constraints are rules that ensure data integrity and prevent invalid data from being inserted into your database. **SQLModel** supports several types of constraints through **SQLAlchemy**.

These constraints are enforced at the **database level**, which means they work regardless of which application is inserting the data. This is particularly important for data consistency and reliability in production systems.

/// info

**SQLModel** uses <a href="https://docs.sqlalchemy.org/en/20/core/constraints.html" class="external-link" target="_blank">SQLAlchemy's constraint system</a> under the hood, giving you access to all the powerful constraint options available in SQLAlchemy.

///

## Unique Constraints

Unique constraints ensure that certain fields or combinations of fields have unique values across all rows in the table.

### Single Column Unique Constraints

The simplest way to add a unique constraint is using the `unique` parameter in the `Field()` function:

{* ./docs_src/advanced/constraints/tutorial001_py310.py ln[6:11] hl[8] *}

In this example, the `name` field must be unique across all heroes. If you try to insert a hero with a name that already exists, the database will raise an error.

✅ **Valid examples:**
* Two heroes with names "Deadpond" and "Spider-Boy" 
* Heroes with the same age but different names

🚫 **Invalid examples:**
* Two heroes both named "Deadpond"
* Inserting a hero with a name that already exists in the database

### Multi-Column Unique Constraints

Sometimes you want a combination of fields to be unique, even though each individual field can have duplicate values. You can achieve this using `__table_args__` with `UniqueConstraint`:

{* ./docs_src/advanced/constraints/tutorial002_py310.py ln[7:13] hl[8] *}

In this example, the combination of `name` and `age` must be unique. This means you can have multiple heroes with the same name (as long as they have different ages), and you can have multiple heroes with the same age (as long as they have different names).

✅ **Valid examples:**
* "Spider-Boy" aged 16 and "Spider-Boy" aged 25 (same name, different ages)
* "Spider-Boy" aged 16 and "Iron Man" aged 16 (different names, same age)

🚫 **Invalid examples:**
* Two heroes both named "Spider-Boy" and both aged 16

/// tip

You can include as many fields as needed in a `UniqueConstraint`. For example: `UniqueConstraint("name", "age", "team")` would make the combination of all three fields unique.

///

## Check Constraints

Check constraints allow you to define custom validation rules using SQL expressions. These are more flexible than basic type validation and can enforce business rules at the database level.

{* ./docs_src/advanced/constraints/tutorial003_py310.py ln[7:13] hl[8] *}

In this example, the check constraint ensures that the `age` field cannot be negative. The constraint has a name (`age_non_negative`) which makes error messages clearer and allows you to reference it later if needed.

✅ **Valid examples:**
* Heroes with age 0, 16, 25, 100, etc.
* Any non-negative integer for age

🚫 **Invalid examples:**
* Heroes with negative ages like -5, -1, etc.

/// info

Check constraints can use any valid SQL expression supported by your database. Common examples include:

- **Range checks:** `age BETWEEN 0 AND 150`
- **String length:** `LENGTH(name) >= 2`
- **Pattern matching:** `email LIKE '%@%'`
- **Value lists:** `status IN ('active', 'inactive', 'pending')`

///

### Naming Check Constraints

It's a good practice to always give your check constraints descriptive names using the `name` parameter. This makes debugging easier when constraint violations occur:

```python
CheckConstraint("age >= 0", name="age_non_negative")
CheckConstraint("LENGTH(name) >= 2", name="name_min_length")
CheckConstraint("email LIKE '%@%'", name="email_format")
```

## Combining Multiple Constraints

You can combine different types of constraints in the same table by adding multiple constraint objects to `__table_args__`:

{* ./docs_src/advanced/constraints/tutorial004_py310.py ln[7:16] hl[8:12] *}

This example combines:
- A unique constraint on the combination of `name` and `age`
- A check constraint ensuring age is non-negative
- A check constraint ensuring name has at least 2 characters

/// tip

When combining constraints, remember that **all constraints must be satisfied** for data to be inserted successfully. Design your constraints carefully to ensure they work together and don't create impossible conditions.

///

## Constraint Violation Errors

When constraints are violated, SQLAlchemy will raise exceptions. It's good practice to handle these in your application:

```python
from sqlalchemy.exc import IntegrityError

try:
    with Session(engine) as session:
        # Trying to insert duplicate data
        hero = Hero(name="Deadpond", age=48, secret_name="Dive Wilson")
        session.add(hero)
        session.commit()
except IntegrityError as e:
    print(f"Constraint violation: {e}")
    session.rollback()
```

## Database Support

/// warning

Not all databases support all types of constraints equally:

- **SQLite:** Supports unique constraints and basic check constraints, but has limitations with some complex SQL expressions
- **PostgreSQL:** Full support for all constraint types with rich SQL expression support  
- **MySQL:** Good support for most constraints, with some syntax differences in check constraints
- **SQL Server:** Full support for all constraint types

Always test your constraints with your target database to ensure compatibility.

///

## Best Practices

🎯 **Use meaningful constraint names** - This makes debugging easier when violations occur

🎯 **Combine field-level and table-level constraints** - Use `Field(unique=True)` for simple cases and `__table_args__` for complex ones

🎯 **Consider performance** - Unique constraints automatically create indexes, which can improve query performance

🎯 **Handle constraint violations gracefully** - Always wrap database operations in try-catch blocks when constraints might be violated

🎯 **Document your constraints** - Make sure your team understands what business rules the constraints enforce

/// info

Remember that **SQLModel** constraints are implemented using **SQLAlchemy**, so you have access to all the power and flexibility of SQLAlchemy's constraint system. For more advanced use cases, check the <a href="https://docs.sqlalchemy.org/en/20/core/constraints.html" class="external-link" target="_blank">SQLAlchemy constraints documentation</a>.

///