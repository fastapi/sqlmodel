# Relationship Attributes - Intro

In the previous chapters we discussed how to manage databases with tables that have **relationships** by using fields (columns) with **foreign keys** pointing to other columns.

And then we read the data together with `select()` and using `.where()` or `.join()` to connect it.

Now we will see how to use **Relationship Attributes**, an extra feature of **SQLModel** (and SQLAlchemy), to work with the data in the database in a much more familiar way, and closer to normal Python code.

/// info

When I say "**relationship**" I mean the standard dictionary term, of data related to other data.

I'm not using the term "**relation**" that is the technical, academical, SQL term for a single table.

///

And using those **relationship attributes** is where a tool like **SQLModel** really shines. ✨
