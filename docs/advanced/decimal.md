# Decimal Numbers

In some cases you might need to be able to store decimal numbers with guarantees about the precision.

This is particularly important if you are storing things like **currencies**, **prices**, **accounts**, and others, as you would want to know that you wouldn't have rounding errors.

As an example, if you open Python and sum `1.1` + `2.2` you would expect to see `3.3`, but you will actually get `3.3000000000000003`:

```Python
>>> 1.1 + 2.2
3.3000000000000003
```

This is because of the way numbers are stored in "ones and zeros" (binary). But Python has a module and some types to have strict decimal values. You can read more about it in the official <a href="https://docs.python.org/3/library/decimal.html" class="external-link" target="_blank">Python docs for Decimal</a>.

Because databases store data in the same ways as computers (in binary), they would have the same types of issues. And because of that, they also have a special **decimal** type.

In most cases this would probably not be a problem, for example measuring views in a video, or the life bar in a videogame. But as you can imagine, this is particularly important when dealing with **money** and **finances**.

## Decimal Types

Pydantic has special support for `Decimal` types using the <a href="https://pydantic-docs.helpmanual.io/usage/types/#arguments-to-condecimal" class="external-link" target="_blank">`condecimal()` special function</a>.

!!! tip
    Pydantic 1.9, that will be released soon, has improved support for `Decimal` types, without needing to use the `condecimal()` function.

    But meanwhile, you can already use this feature with `condecimal()` in **SQLModel** it as it's explained here.

When you use `condecimal()` you can specify the number of decimal places and digits to support. They will be validated by Pydantic (for example when using FastAPI) and the same information will also be used for the database columns.

!!! info
    For the database, **SQLModel** will use <a href="https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.DECIMAL" class="external-link" target="_blank">SQLAlchemy's `DECIMAL` type</a>.

## Decimals in SQLModel

Let's say that each hero in the database will have an amount of money. We could make that field a `Decimal` type using the `condecimal()` function:

```{.python .annotate hl_lines="12" }
{!./docs_src/advanced/decimal/tutorial001.py[ln:1-12]!}

# More code here later 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

</details>

## Create models with Decimals

When creating new models you can actually pass normal (`float`) numbers, Pydantic will automatically convert them to `Decimal` types, and **SQLModel** will store them as `Decimal` types in the database (using SQLAlchemy).

```Python hl_lines="4-6"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001.py[ln:25-35]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

</details>

## Select Decimal data

Then, when working with Decimal types, you can confirm that they indeed avoid those rounding errors from floats:

```Python hl_lines="15-16"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001.py[ln:38-51]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

</details>

## Review the results

Now if you run this, instead of printing the unexpected number `3.3000000000000003`, it prints `3.300`:

<div class="termy">

```console
$ python app.py

// Some boilerplate and previous output omitted 😉

// The type of money is Decimal('1.100')
Hero 1: id=1 secret_name='Dive Wilson' age=None name='Deadpond' money=Decimal('1.100')

// More output omitted here 🤓

// The type of money is Decimal('1.100')
Hero 2: id=3 secret_name='Tommy Sharp' age=48 name='Rusty-Man' money=Decimal('2.200')

// No rounding errors, just 3.3! 🎉
Total money: 3.300
```

</div>

!!! warning
    Although Decimal types are supported and used in the Python side, not all databases support it. In particular, SQLite doesn't support decimals, so it will convert them to the same floating `NUMERIC` type it supports.

    But decimals are supported by most of the other SQL databases. 🎉
