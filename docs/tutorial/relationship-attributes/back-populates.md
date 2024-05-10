# Relationship back_populates

Now you know how to use the **relationship attributes** to manipulate connected data in the database! 🎉

Let's now take a small step back and review how we defined those `Relationship()` attributes again, let's clarify that `back_populates` argument. 🤓

## Relationship with `back_populates`

So, what is that `back_populates` argument in each `Relationship()`?

The value is a string with the name of the attribute in the **other** model class.

<img src="/img/tutorial/relationships/attributes/back-populates.svg">

That tells **SQLModel** that if something changes in this model, it should change that attribute in the other model, and it will work even before committing with the session (that would force a refresh of the data).

Let's understand that better with an example.

## An Incomplete Relationship

Let's see how that works by writing an **incomplete** version first, without `back_populates`:

//// tab | Python 3.10+

```Python hl_lines="9  19"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:1-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py!}
```

////

///

## Read Data Objects

Now, we will get the **Spider-Boy** hero and, *independently*, the **Preventers** team using two `select`s.

As you already know how this works, I won't separate that in a select `statement`, `results`, etc. Let's use the shorter form in a single call:

//// tab | Python 3.10+

```Python hl_lines="5-7  9-11"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:103-111]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="5-7  9-11"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:105-113]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5-7  9-11"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:105-113]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py!}
```

////

///

/// tip

When writing your own code, this is probably the style you will use most often, as it's shorter, more convenient, and you still get all the power of autocompletion and inline errors.

///

## Print the Data

Now, let's print the current **Spider-Boy**, the current **Preventers** team, and particularly, the current **Preventers** list of heroes:

//// tab | Python 3.10+

```Python hl_lines="13-15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:103-115]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="13-15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:105-117]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13-15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:105-117]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py!}
```

////

///

Up to this point, it's all good. 😊

In particular, the result of printing `preventers_team.heroes` is:

``` hl_lines="3"
Preventers Team Heroes: [
        Hero(name='Rusty-Man', age=48, id=2, secret_name='Tommy Sharp', team_id=2),
        Hero(name='Spider-Boy', age=None, id=3, secret_name='Pedro Parqueador', team_id=2),
        Hero(name='Tarantula', age=32, id=6, secret_name='Natalia Roman-on', team_id=2),
        Hero(name='Dr. Weird', age=36, id=7, secret_name='Steve Weird', team_id=2),
        Hero(name='Captain North America', age=93, id=8, secret_name='Esteban Rogelios', team_id=2)
]
```

Notice that we have **Spider-Boy** there.

## Update Objects Before Committing

Now let's update **Spider-Boy**, removing him from the team by setting `hero_spider_boy.team = None` and then let's print this object again:

//// tab | Python 3.10+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:103-104]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:117-121]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:119-123]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:119-123]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py!}
```

////

///

The first important thing is, we *haven't committed* the hero yet, so accessing the list of heroes would not trigger an automatic refresh.

But in our code, in this exact point in time, we already said that **Spider-Boy** is no longer part of the **Preventers**. 🔥

/// tip

We could revert that later by not committing the **session**, but that's not what we are interested in here.

///

Here, at this point in the code, in memory, the code expects **Preventers** to *not include* **Spider-Boy**.

The output of printing `hero_spider_boy` without team is:

```
Spider-Boy without team: name='Spider-Boy' age=None id=3 secret_name='Pedro Parqueador' team_id=2 team=None
```

Cool, the team is set to `None`, the `team_id` attribute still has the team ID until we save it. But that's okay as we are now working mainly with the **relationship attributes** and the objects. ✅

But now, what happens when we print the `preventers_team.heroes`?

``` hl_lines="3"
Preventers Team Heroes again: [
        Hero(name='Rusty-Man', age=48, id=2, secret_name='Tommy Sharp', team_id=2),
        Hero(name='Spider-Boy', age=None, id=3, secret_name='Pedro Parqueador', team_id=2, team=None),
        Hero(name='Tarantula', age=32, id=6, secret_name='Natalia Roman-on', team_id=2),
        Hero(name='Dr. Weird', age=36, id=7, secret_name='Steve Weird', team_id=2),
        Hero(name='Captain North America', age=93, id=8, secret_name='Esteban Rogelios', team_id=2)
]
```

Oh, no! 😱 **Spider-Boy** is still listed there!

## Commit and Print

Now, if we commit it and print again:

//// tab | Python 3.10+

```Python hl_lines="8-9  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:103-104]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py[ln:123-130]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8-9  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py[ln:125-132]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8-9  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py[ln:125-132]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial001.py!}
```

////

///

When we access `preventers_team.heroes` after the `commit`, that triggers a refresh, so we get the latest list, without **Spider-Boy**, so that's fine again:

```
INFO Engine SELECT hero.id AS hero_id, hero.name AS hero_name, hero.secret_name AS hero_secret_name, hero.age AS hero_age, hero.team_id AS hero_team_id
FROM hero
WHERE ? = hero.team_id
2021-08-13 11:15:24,658 INFO sqlalchemy.engine.Engine [cached since 0.1924s ago] (2,)

Preventers Team Heroes after commit: [
        Hero(name='Rusty-Man', age=48, id=2, secret_name='Tommy Sharp', team_id=2),
        Hero(name='Tarantula', age=32, id=6, secret_name='Natalia Roman-on', team_id=2),
        Hero(name='Dr. Weird', age=36, id=7, secret_name='Steve Weird', team_id=2),
        Hero(name='Captain North America', age=93, id=8, secret_name='Esteban Rogelios', team_id=2)
]
```

There's no **Spider-Boy** after committing, so that's good. 😊

But we still have that inconsistency in that previous point above.

If we use the objects before committing, we could end up having errors. 😔

Let's fix that. 🤓

## Fix It Using `back_populates`

That's what `back_populates` is for. ✨

Let's add it back:

//// tab | Python 3.10+

```Python hl_lines="9  19"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:1-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py!}
```

////

///

And we can keep the rest of the code the same:

//// tab | Python 3.10+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:103-104]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:117-121]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:119-123]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8  12"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:105-106]!}

        # Code here omitted 👈

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:119-123]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py!}
```

////

///

/// tip

This is the same section where we updated `hero_spider_boy.team` to `None` but we *haven't committed* that change yet.

The same section that caused a problem before.

///

## Review the Result

This time, **SQLModel** (actually SQLAlchemy) will be able to notice the change, and **automatically update the list of heroes** in the team, even before we commit.

That second print would output:

```
Preventers Team Heroes again: [
        Hero(name='Rusty-Man', age=48, id=2, secret_name='Tommy Sharp', team_id=2),
        Hero(name='Tarantula', age=32, id=6, secret_name='Natalia Roman-on', team_id=2),
        Hero(name='Dr. Weird', age=36, id=7, secret_name='Steve Weird', team_id=2),
        Hero(name='Captain North America', age=93, id=8, secret_name='Esteban Rogelios', team_id=2)
]
```

Notice that now **Spider-Boy** is not there, we fixed it with `back_populates`! 🎉

## The Value of `back_populates`

Now that you know why `back_populates` is there, let's review the exact value again.

It's quite simple code, it's just a string, but it might be confusing to think exactly *what* string should go there:

//// tab | Python 3.10+

```Python hl_lines="9  19"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:1-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:1-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11  21"
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:1-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py!}
```

////

///

The string in `back_populates` is the name of the attribute *in the other* model, that will reference *the current* model.

<img src="/img/tutorial/relationships/attributes/back-populates.svg">

So, in the class `Team`, we have an attribute `heroes` and we declare it with `Relationship(back_populates="team")`.

//// tab | Python 3.10+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:4-9]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:6-11]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="8"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:6-11]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py!}
```

////

///

The string in `back_populates="team"` refers to the attribute `team` in the class `Hero` (the other class).

And, in the class `Hero`, we declare an attribute `team`, and we declare it with `Relationship(back_populates="heroes")`.

So, the string `"heroes"` refers to the attribute `heroes` in the class `Team`.

//// tab | Python 3.10+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py[ln:12-19]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py[ln:14-21]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="10"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py[ln:14-21]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial002.py!}
```

////

///

/// tip

Each **relationship attribute** points to the other one, in the other model, using `back_populates`.

///

Although it's simple code, it can be confusing to think about 😵, because the same line has concepts related to both models in multiple places:

* Just by being in the **current** model, the line has something to do with the current model.
* The name of the attribute is about the **other** model.
* The type annotation is about the **other** model.
* And the `back_populates` refers to an attribute in the **other** model, that points to the **current** model.

## A Mental Trick to Remember `back_populates`

A mental trick you can use to remember is that the string in `back_populates` is always about the current model class you are editing. 🤓

So, if you are in the class `Hero`, the value of `back_populates` for any relationship attribute connecting to **any** other table (to any other model, it could be `Team`, `Weapon`, `Powers`, etc) will still always refer to this same class.

So, `back_populates` would most probably be something like `"hero"` or `"heroes"`.

<img src="/img/tutorial/relationships/attributes/back-populates2.svg">

//// tab | Python 3.10+

```Python hl_lines="3  10  13  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003_py310.py[ln:27-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3  10  13  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003_py39.py[ln:29-41]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  10  13  15"
# Code above omitted 👆

{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003.py[ln:29-41]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/relationship_attributes/back_populates/tutorial003.py!}
```

////

///
