# Database to Code (ORMs)

Here I'll tell you how **SQLModel** interacts with the database, why you would want to use it (or use a similar tool), and how it relates to SQL.

## SQL Inline in Code

Let's check this example of a simple SQL query to get all the data from the `hero` table:

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

This SQL language has a little **caveat**. It was not designed to be mixed with normal code in a programming language like Python. 🚨

So, if you are working with Python, the simplest option would be to put SQL code inside a string, and send that string directly to the database.

```Python
statement = "SELECT * FROM hero;"

results = database.execute(statement)
```

But in that case, you wouldn't have editor support, inline errors, autocompletion, etc. Because for the editor, the SQL statement is just a string of text. If you have an error, the editor wouldn't be able to help. 😔

And even more importantly, in most of the cases, you would send the SQL strings with modifications and parameters. For example, to get the data for a *specific item ID*, a *range of dates*, etc.

And in most cases, the parameters your code uses to query or modify the data in the database come, in some way, from an external user.

For example, check this SQL query:

```SQL
SELECT *
FROM hero
WHERE id = 2;
```

It is using the ID parameter `2`. That number `2` probably comes, in some way, from a user input.

The user is probably, in some way, telling your application:

> Hey, I want to get the hero with ID:

```SQL
2
```

And the  would be this table (with a single row):

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id</th>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1</td>
</tr>
</table>

### SQL Injection

But let's say that your code takes whatever the external user provides and puts it inside the SQL string before sending it to the database. Something like this:

```Python
# Never do this! 🚨 Continue reading.

user_id = input("Type the user ID: ")

statement = f"SELECT * FROM hero WHERE id = {user_id};"

results = database.execute(statement)
```

If the external user is actually an attacker, they could send you a malicious SQL string that does something terrible like deleting all the records. That's called a "**SQL Injection**".

For example, imagine that this new attacker user says:

> Hey, I want to get the hero with ID:

```SQL
2; DROP TABLE hero
```

Then the code above that takes the user input and puts it in SQL would actually send this to the database:

```SQL
SELECT * FROM hero WHERE id = 2; DROP TABLE hero;
```

Check that section added at the end. That's another entire SQL statement:

```SQL
DROP TABLE hero;
```

That is how you tell the database in SQL to delete the entire table `hero`.

<a href="http://www.nooooooooooooooo.com/" class="external-link" target="_blank">Nooooo!</a> We lost all the data in the `hero` table! 💥😱

### SQL Sanitization

The process of making sure that whatever the external user sends is safe to use in the SQL string is called **sanitization**.

It comes by default in **SQLModel** (thanks to SQLAlchemy). And many other similar tools would also provide that functionality among many other features.

Now you are ready for <a href="https://xkcd.com/327/" class="external-link" target="_blank">a  joke from xkcd</a>:

![Exploits of a Mom](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)

## SQL with SQLModel

With **SQLModel**, instead of writing SQL statements directly, you use Python classes and objects to interact with the database.

For example, you could ask the database for the same hero with ID `2` with this code:

```Python
user_id = input("Type the user ID: ")

session.exec(
    select(Hero).where(Hero.id == user_id)
).all()
```

If the user provides this ID:

```SQL
2
```

...the  would be this table (with a single row):

<table>
<tr>
<th>id</th><th>name</th><th>secret_name</th><th>age</th><th>team_id</th>
</tr>
<tr>
<td>2</td><td>Spider-Boy</td><td>Pedro Parqueador</td><td>null</td><td>1</td>
</tr>
</table>

### Preventing SQL Injections

If the user is an attacker and tries to send this as the "ID":

```SQL
2; DROP TABLE hero
```

Then **SQLModel** will convert that to a literal string `"2; DROP TABLE hero"`.

And then, it will tell the SQL Database to try to find a record with that exact ID instead of injecting the attack.

The difference in the final SQL statement is subtle, but it changes the meaning completely:

```SQL
SELECT * FROM hero WHERE id = "2; DROP TABLE hero;";
```

!!! tip
    Notice the double quotes (`"`) making it a string instead of more raw SQL.

The database will not find any record with that ID:

```SQL
"2; DROP TABLE hero;"
```

Then the database will send an empty table as the result because it didn't find any record with that ID.

Then your code will continue to execute and calmly tell the user that it couldn't find anything.

But we never deleted the `hero` table. 🎉

!!! info
    Of course, there are also other ways to do SQL data sanitization without using a tool like **SQLModel**, but it's still a nice feature you get by default.

### Editor Support

Check that Python snippet above again.

Because we are using **standard Python classes and objects**, your editor will be able to provide you with autocompletion, inline errors, etc.

For example, let's say you wanted to query the database to find a hero based on the secret identity.

Maybe you don't remember how you named the column. Maybe it was:

* `secret_identity`?

...or was it:

* `secretidentity`?

...or:

* `private_name`?
* `secret_name`?
* `secretname`?

If you type that in SQL strings in your code, your editor **won't be able to help you**:

```SQL
statement = "SELECT * FROM hero WHERE secret_identity = 'Dive Wilson';"

results = database.execute(statement)
```

...your editor will see that as a **long string** with some text inside, and it will **not be able to autocomplete** or detect the error in `secret_identity`.

But if you use common Python classes and objects, your editor will be able to help you:

```Python
database.execute(
    select(Hero).where(Hero.secret_name == "Dive Wilson")
).all()
```

<img class="shadow" src="/img/db-to-code/autocompletion01.png">


## ORMs and SQL

These types of libraries like **SQLModel** (and of course, SQLAlchemy) that translate between SQL and code with classes and objects are called **ORMs**.

**ORM** means **Object-Relational Mapper**.

This is a very common term, but it also comes from quite technical and **academical** concepts 👩‍🎓:

* **Object**: refers to code with classes and instances, normally called "Object Oriented Programming", that's why the "**Object**" part.

For example this class is part of that **Object** Oriented Programming:

```Python
class Hero(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

* **Relational**: refers to the **SQL Databases**. Remember that they are also called **Relational Databases**, because each of those tables is also called a "**relation**"? That's where the "**Relational**" comes from.

For example this **Relation** or table:

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

* **Mapper**: this comes from Math, when there's something that can convert from some set of things to another, that's called a "**mapping function**". That's where the **Mapper** comes from.

![Squares to Triangles Mapper](/img/db-to-code/mapper.svg)

We could also write a **mapping function** in Python that converts from the *set of lowercase letters* to the *set of uppercase letters*, like this:

```Python
def map_lower_to_upper(value: str):
    return value.upper()
```

It's actually a simple idea with a very academic and mathematical name. 😅

So, an **ORM** is a library that translates from SQL to code, and from code to SQL. All using classes and objects.

There are many ORMs available apart from **SQLModel**, you can read more about some of them in [Alternatives, Inspiration and Comparisons](alternatives.md){.internal-link target=_blank}

## SQL Table Names

!!! info "Technical Background"
    This is a bit of boring background for SQL purists. Feel free to skip this section. 😉

When working with pure SQL, it's common to name the tables in plural. So, the table would be named `heroes` instead of `hero`, because it could contain multiple rows, each with one hero.

Nevertheless, **SQLModel** and many other similar tools can generate a table name automatically from your code, as you will see later in the tutorial.

But this name will be derived from a class name. And it's common practice to use **singular** names for classes (e.g. `class Hero`, instead of `class Heroes`). Using singular names for classes like `class Hero` also makes your code more intuitive.

You will see **your own code** a lot more than the internal table names, so it's probably better to keep the code/class convention than the SQL convention.

So, to keep things consistent, I'll keep using the same table names that **SQLModel** would have generated.

!!! tip
    You can also override the table name. You can read about it in the Advanced User Guide.