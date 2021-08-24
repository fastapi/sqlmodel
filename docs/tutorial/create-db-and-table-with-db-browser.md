# Create a Table with SQL

Let's get started!

We will:

* Create a SQLite database with **DB Browser for SQLite**
* Create a table in the database with **DB Browser for SQLite**

We'll add data later. For now, we'll create the database and the first table structure.

We will create a table to hold this data:

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th>
</tr>
<tr>
<td>1</td><td>Deadpond</td><td>Dive Wilson</td><td>null</td>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td>
</tr>
<tr>
<td>3</td><td>Rusty-Man</td><td>Tommy Sharp</td><td>48</td>
</tr>
</table>

## Create a Database

**SQLModel** and SQLAlchemy are based on SQL.

They are designed to help you with using SQL through Python classes and objects. But it's still always very useful to understand SQL.

So let's start with a simple, pure SQL example.

Open **DB Browser for SQLite**.

Click the button <kbd>New Database</kbd>.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image001.png">

A dialog should show up. Go to the [project directory you created](./index.md#create-a-project){.internal-link target=_blank} and save the file with a name of `database.db`.

!!! tip
    It's common to save SQLite database files with an extension of `.db`. Sometimes also `.sqlite`.

## Create a Table

After doing that, it might prompt you to create a new table right away.

If it doesn't, click the button <kbd>Create Table</kbd>.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image002.png">

Then you will see the dialog to create a new table.

So, let's create a new table called `hero` with the following columns:

* `id`: an `INTEGER` that will be the **primary key** (check `PK` ✅).
* `name`: a `TEXT`, it should be `NOT NULL` (check `NN` ✅), so, it should always have a value.
* `secret_name`: a `TEXT`, it should be `NOT NULL` too (check `NN` ✅).
* `age`: an `INTEGER`, this one can be `NULL`, so you don't have to check anything else.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image003.png">

Click <kbd>OK</kbd> to create the table.

While you click on the <kbd>Add</kbd> button and add the information, it will create and update the SQL statement that is executed to create the table:

```{ .sql .annotate }
CREATE TABLE "hero" ( --(1)
  "id"  INTEGER, --(2)
  "name"  TEXT NOT NULL, --(3)
  "secret_name" TEXT NOT NULL, --(4)
  "age" INTEGER, --(5)
  PRIMARY KEY("id") --(6)
); --(7)
```

1. Create a table with the name `hero`. Also notice that the columns for this table are declared inside the parenthesis " `(`" that starts here.
2. The `id` column, an `INTEGER`. This is declared as the primary key at the end.
3. The `name` column, a `TEXT`, and it should always have a value `NOT NULL`.
4. The `secret_name` column, another `TEXT`, also `NOT NULL`.
5. The `age` column, an `INTEGER`. This one doesn't have `NOT NULL`, so it *can* be `NULL`.
6. The `PRIMARY KEY` of all this is the `id` column.
7. This is the end of the SQL table, with the final parenthesis "`)`". It also has the semicolon "`;`" that marks the end of the SQL statement. There could be more SQL statements in the same SQL string.

Now you will see that it shows up in the list of Tables with the columns we specified. 🎉

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image004.png">

The only step left is to click <kbd>Write Changes</kbd> to save the changes to the file.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image005.png">

After that, the new table is saved in this database on the file `./database.db`.

## Confirm the Table

Let's confirm that it's all saved.

First click the button <kbd>Close Database</kbd> to close the database.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image006.png">

Now click on <kbd>Open Database</kbd> to open the database again, and select the same file `./database.db`.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image007.png">

You will see again the same table we created.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image008.png">

## Create the Table again, with SQL

Now, to see how is it that SQL works, let's create the table again, but with SQL.

Click the <kbd>Close Database</kbd> button again.

And delete that `./database.db` file in your project directory.

And click again on <kbd>New Database</kbd>.

This time, if you see the dialog to create a new table, just close it by clicking the <kbd>Cancel</kbd> button.

And now, go to the tab <kbd>Execute SQL</kbd>.

Write the same SQL that was generated in the previous step:

```SQL
CREATE TABLE "hero" (
  "id"  INTEGER,
  "name"  TEXT NOT NULL,
  "secret_name" TEXT NOT NULL,
  "age" INTEGER,
  PRIMARY KEY("id")
);
```

Then click the "Execute all" <kbd>▶</kbd> button.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image009.png">

You will see the "execution finished successfully" message.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image010.png">

And if you go back to the <kbd>Database Structure</kbd> tab, you will see that you effectively created again the same table.

<img class="shadow" src="/img/create-db-and-table-with-db-browser/image008.png">

## Learn More SQL

I will keep showing you small bits of SQL through this tutorial. And you don't have to be a SQL expert to use **SQLModel**.

But if you are curious and want to get a quick overview of SQL, I recommend the visual documentation from SQLite, on <a href="https://www.sqlite.org/lang.html" class="external-link" target="_blank">SQL As Understood By SQLite</a>.

You can start with <a href="https://www.sqlite.org/lang_createtable.html" class="external-link" target="_blank">`CREATE TABLE`</a>.

Of course, you can also go and take a full SQL course or read a book about SQL, but you don't need more than what I'll explain here on the tutorial to start being productive with **SQLModel**. 🤓

## Recap

We saw how to interact with SQLite databases in files using **DB Browser for SQLite** in a visual user interface.

We also saw how to use it to write some SQL directly to the SQLite database. This will be useful to verify the data in the database is looking correclty, to debug, etc.

In the next chapters we will start using **SQLModel** to interact with the database, and we will continue to use **DB Browser for SQLite** at the same time to look at the database underneath. 🔍
