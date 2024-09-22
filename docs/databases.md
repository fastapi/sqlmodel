# Intro to Databases

/// info

Are you a seasoned developer and already know everything about databases? 🤓

Then you can skip to the next sections right away.

///

If you don't know everything about databases, here's a quick overview.

You can always study much more on your own later.

But this should help you start using databases and being productive with **SQLModel**. 🚀

## What is a Database

So, what is a database?

A **database** is a system to store and manage data in a structured and very efficient way.

/// tip

It's very common to abbreviate the word "database" as **"DB"**.

///

As there's a lot of information about databases, and it can get very technical and academic, I'll give you a quick overview about some of the main concepts here.

I'll even tell you a bit about different types of databases, including the ones not covered by SQLModel ("NoSQL" databases).

## Why Use a Database

When starting to program, it might **not be obvious** why having a database apart from the code for your program is a **good idea**. Let's start with that.

/// tip

If that's obvious to you, just continue in the next section below. 👇

///

In your code you already have **variables**, **dictionaries**, **lists**, etc. They all store **data** in some way already. Why would you need to have a separate database?

If you look closely, your code is **static**, it doesn't really change over time *once you run it*. Of course, you change the code frequently, adding features, etc, but once you start Python running your code, the program stays as it was when you started it. And if you change the code, the program will only change **once you run it again**.

And even if you change things in variables, once the program terminates, all that data that was in **memory** is **gone**. 🔥

In most of the cases, the objective of your program is to do something with data *outside* of the program.

* It could be just moving **files** from one place to the other.
* Or it could be taking data from the user in the **terminal** and showing it differently.
* Or a **web API** that takes some data and process it in some way, etc.

In most cases, the data *comes from outside* the program or *ends outside the program* (for example, shown on the screen, in a file, etc).

In many cases, you need your program to be able to **create** and store data, **read** it, **update** it, **delete** it, etc.

You could do all that by reading and writing to files from your code. And that works in simple cases. But for most complex systems with data that is a bit more **complex** that strategy is not very efficient. And you would have to deal with a lot of **caveats**, keeping the data in sync, making sure it is safely stored, etc.

Databases are designed to **solve these problems**, making the process of handling data much more efficient, and independent of your code. ✨

## How to Interact with a Database

There are many databases of many types.

### A single file database

A database could be a single file called `heroes.db`, managed with code in a very efficient way. An example would be SQLite, more about that in a bit.

![database as a single file](/img/databases/single-file.svg)

### A server database

A database could also be a system running as an application on a server, handling multiple files internally in optimized formats.

Like a web server, but communicating in a custom and very efficient way. That is the most common type of database interaction.

In this case, your code would talk to this server application instead of reading or modifying files directly.

The database could be located in a different server/machine:

![database in an external server](/img/databases/external-server.svg)

Or the database could be located in the same server/machine:

![database in the same server](/img/databases/same-server.svg)

The most important aspect of these types of databases is that **your code doesn't read or modify** the files containing the data directly.

Instead, your code communicates with the database application and that database application is the one that actually reads and modifies its data files. This is because this database application is normally **much more efficient** than what your code could be.

Some examples of databases that work like this could be **PostgreSQL**, **MySQL**, or **MongoDB**.

### Distributed servers

In some cases, the database could even be a group of server applications running on different machines, working together and communicating between them to be more efficient and handle more data.

In this case, your code would talk to one or more of these server applications running on different machines.

![distributed database in multiple servers](/img/databases/multiple-servers.svg)

Most of the databases that work as server applications also support multiple servers in one way or another.

Having distributed systems also creates additional challenges, so there's a high chance that you would first interact with a single server application or one based on a single file.

## SQL Databases

We already talked about the different ways to interact with a database and how they handle files, etc. That applies to most or all of the databases.

But there's another way to categorize databases that is very important. As you can imagine, there are many types of databases and many databases in each group. But in general, they can be separated in two big groups: "SQL Databases" and "NoSQL Databases".

We will get to why the name "SQL" in a bit, but first, let's see what is it all about.

### SQLModel for SQL Databases

**SQLModel** is a tool to help you with **SQL Databases**.

It cannot help you much with **NoSQL Databases**. Nevertheless, I'll explain a bit about them here.

## Invent SQL Databases

A long time ago, some smart people realized that a great way to store data was putting it in different tables.

And by "table" I mean just data in a grid, with different columns and rows, pretty much like a single spreadsheet.

Each row would represent a specific item or **record**. And each column would represent a specific attribute or field of that record.

### An example of a big table

Let's imagine that we need to store some data about heroes.

If we worked with a single table to store our heroes, it could be like this:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team</th><th>headquarters</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>Z-Factor</td><td>Sister Margaret's Bar</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>Preventers</td><td>Sharp Tower</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>Preventers</td><td>Sharp Tower</td>
</tr>
</table>

That's probably what we would have to do with a single table, for example, with a single spreadsheet.

But there are some problems with this. Let's check some.

#### Single table problems

Imagine that they decided to rename the "Sharp Tower" to "Preventers Tower".

Now we would have to update that in two places.

What happens if our code starts to update that name in one place and suddenly there's a power outage and the computer goes off?

We could end up with inconsistent information, having one place saying "Preventers Tower" and the other one saying "Sharp Tower":

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team</th><th>headquarters</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>Z-Force</td><td>Sister Margaret's Bar</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>Preventers</td><td>Preventers Tower ✅</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>Preventers</td><td>Sharp Tower 🚨</td>
</tr>
</table>

And now imagine that we need to add a new hero called "Mahjong" that is part of the team "Z-Force".

We could forget the name of the team and end up adding "Mahjong" with an invalid team name, for example "Y-Force".

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team</th><th>headquarters</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>Z-Force</td><td>Sister Margaret's Bar</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>Preventers</td><td>Preventers Tower</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>Preventers</td><td>Sharp Tower</td>
</tr>
<tr>
<td>4</td><td>Mahjong</td><td>Neena Thurgirl</td><td>31</td><td>Y-Force 🚨</td><td>Sister Margaret's Bar</td>
</tr>
</table>

And what if a single hero belongs to two teams? We wouldn't have an easy way to put this into a single big table.

### Multiple tables

But these and other problems could be solved better by having the data in multiple tables.

So, instead of having a single table with all the data, we could have one table for the heroes and one for teams, and a way to connect one with the other.

The table for the teams could look like this:

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

Now, the table for the heroes would look almost the same. But remember that we mentioned that we need a way to connect the two tables?

The table for the heroes would now have another column `team_id`. This column shows the relationship from each row (from each hero) to the team they belong to.

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id ✨</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>2 ✨</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1 ✨</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>1 ✨</td>
</tr>
</table>

#### Identifications - Primary Key

In the example above, each one of the rows has an <abbr title='abbreviated from the word "identification", in many cases written as "ID"'>`id`</abbr>. Each ID is unique per table and identifies that particular row.

These SQL databases require having a unique way to identify each row in a table. It could be a combination of columns that is unique, but commonly it is just one single column. This is called the "**primary key**" of the table.

The **primary key** is frequently a single column, commonly it's just an integer generated automatically by the database, and in many cases, the column is simply called `id`.

This **primary key**, in this case the column `id`, has to be unique per table. But two different tables could have the same ID. For example, above, both tables have the ID `2` for two different rows, one for "**Z-Force**" in one table and one for "**Spider-Boy**" in the other table, but that's still okay as long as there's a single one per table.

#### Relationships - Foreign Key

Each row in a table has a single **primary key** (in our example a single column `id`).

For example, the table for the teams has the ID `1` for the team `Preventers` and the ID `2` for the team `Z-Force`.

As these **primary key** IDs can uniquely identify each row on the table for teams, we can now go to the table for heroes and refer to those IDs in the table for teams.

<img alt="table relationships" src="/img/databases/relationships.svg">

So, in the table for heroes, we use the `team_id` column to define a relationship to the *foreign* table for teams. Each value in the `team_id` column on the table with heroes will be the same value as the `id` column of one row in the table with teams.

In the table for heroes we have a **primary key** that is the `id`. But we also have another column `team_id` that refers to a **key** in a **foreign** table. There's a technical term for that too, the `team_id` is a "**foreign key**".

### Relations and Relational Databases

The technical and academic term for each one of these tables is a "**relation**".

You might hear that term a lot when talking about these databases.

It doesn't have the meaning that you would use in English of something being related to something else, even though each of these tables is actually "related" to the others.

The technical term **relation** just refers to each one of these tables.

And because of this technical term, these **SQL Databases** are also called **Relational Databases** (in fact, that is the technically correct term). But it still just refers to these databases made with multiple tables.

### SQL - The Language

After developing these ideas of how to store data in multiple tables they also created a **language** that could be used to interact with them.

The language is called **SQL**, the name comes from for **Structured Query Language**.

Nevertheless, the language is not only used to *query* for data. It is also used to create records/rows, to update them, to delete them. And to manipulate the database, create tables, etc.

This language is supported by all these databases that handle multiple tables, that's why they are called **SQL Databases**. Although, each database has small variations in the SQL language they support (*dialect*).

Let's imagine that the table holding the heroes is called the `hero` table. An example of a SQL query to get all the data from it could look like:

```SQL
SELECT *
FROM hero;
```

And that SQL query would return the table:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td><td>2</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td><td>1</td>
</tr>
</table>

### SQLModel for SQL

**SQLModel** is a library that helps you write Python code with regular Python objects, and then it transfers that to **SQL** statements that it sends to a **SQL Database**.

Next, it receives the data and puts it in Python objects that you can continue to use in your code.

I'll tell you more about SQL, SQLModel, how to use them, and how they are related in the next sections.

/// info  | Technical Details

SQLModel is built on top of SQLAlchemy. It is, in fact, just <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> and <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> mixed together with some sugar on top.

///

## NoSQL Databases

Although SQL Databases are the oldest and most commonly used type of database, there's another (very interesting) category, the one of **NoSQL Databases**.

**NoSQL Databases** covers a wide range of different sub-types, including key-value stores, document stores, graph databases, and more.

**SQLModel** can only help you with SQL Databases. So, that's what we'll talk about in the rest of the documentation.
