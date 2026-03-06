# Database Constraints

In some cases you might want to enforce rules about your data directly at the **database level**. For example, making sure that a hero's name is unique, or that their age is never negative. 🦸‍♀️

These rules are called **constraints**, and because they live in the database, they work regardless of which application is inserting the data. This is particularly important for data consistency in production systems.

/// info

**SQLModel** uses <a href="https://docs.sqlalchemy.org/en/20/core/constraints.html" class="external-link" target="_blank">SQLAlchemy's constraint system</a> under the hood, so you have access to all the powerful constraint options available in SQLAlchemy.

///

## Unique Constraints

Let's say you want to make sure that no two heroes can have the same name. The simplest way to do this is with the `unique` parameter in `Field()`:

{* ./docs_src/advanced/constraints/tutorial001_py310.py ln[4:8] hl[6] *}

Now the `name` field must be unique across all heroes. If you try to insert a hero with a name that already exists, the database will raise an error.

So two heroes named "Deadpond" and "Spider-Boy" would work fine, but trying to add a second "Deadpond" would fail.

## Multi-Column Unique Constraints

Sometimes you don't need each individual field to be unique, but you want a **combination** of fields to be unique. For example, you might allow multiple heroes named "Spider-Boy" as long as they have different ages.

You can do this using `__table_args__` with a `UniqueConstraint`:

{* ./docs_src/advanced/constraints/tutorial002_py310.py ln[5:11] hl[6] *}

With this setup, "Spider-Boy" aged 16 and "Spider-Boy" aged 25 are both allowed, because the **combination** of name and age is different. But two heroes both named "Spider-Boy" and both aged 16 would be rejected.

/// tip

You can include as many fields as needed in a `UniqueConstraint`. For example, `UniqueConstraint("name", "age", "team")` would require the combination of all three fields to be unique.

///

## Check Constraints

Check constraints let you define custom validation rules using SQL expressions. This is handy for enforcing business rules, like making sure a hero's age is never negative:

{* ./docs_src/advanced/constraints/tutorial003_py310.py ln[5:11] hl[6] *}

Here we're saying that `age` must be greater than or equal to zero. The `name` parameter gives the constraint a descriptive label, which makes error messages much easier to understand.

So heroes with age 0, 16, or 100 would all be fine, but trying to insert a hero with age -5 would fail.

## Combining Multiple Constraints

You can mix different types of constraints in the same model by adding multiple constraint objects to `__table_args__`:

{* ./docs_src/advanced/constraints/tutorial004_py310.py ln[5:15] hl[6:10] *}

This model has three constraints working together: the combination of `name` and `age` must be unique, age cannot be negative, and the name must be at least 2 characters long. All constraints must be satisfied for data to be inserted successfully.

## What Happens When a Constraint is Violated?

If you try to insert data that breaks a constraint, the database will raise an error. SQLAlchemy wraps this as an `IntegrityError`. Here's what that looks like in practice:

{* ./docs_src/advanced/constraints/tutorial005_py310.py ln[25:38] hl[32:37] *}

When you run this code, you'll see that the first hero is created successfully, but the attempt to create a duplicate fails with a clear error message.

<div class="termy">

```console
$ python app.py

// Some boilerplate and previous output omitted 😉

✅ Created hero: id=1 age=48 secret_name='Dive Wilson' name='Deadpond'
🚫 Constraint violation caught:
   Error: (sqlite3.IntegrityError) UNIQUE constraint failed: hero.name
[SQL: INSERT INTO hero (name, age, secret_name) VALUES (?, ?, ?)]
[parameters: ('Deadpond', 25, 'Wade Wilson')]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
```

</div>

This error handling lets you gracefully manage constraint violations in your application instead of having your program crash unexpectedly. 🛡️

/// warning

Not all databases support all types of constraints equally. In particular, **SQLite** has limitations with some complex SQL expressions in check constraints. Make sure to test your constraints with your target database.

Most other SQL databases like **PostgreSQL** and **MySQL** have full or near-full support. 🎉

///
