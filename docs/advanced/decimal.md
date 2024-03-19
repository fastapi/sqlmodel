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

Pydantic has special support for <a href="https://docs.pydantic.dev/latest/api/standard_library_types/#decimaldecimal" class="external-link" target="_blank">`Decimal` types</a>.

When you use `Decimal` you can specify the number of digits and decimal places to support in the `Field()` function. They will be validated by Pydantic (for example when using FastAPI) and the same information will also be used for the database columns.

/// info

For the database, **SQLModel** will use <a href="https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DECIMAL" class="external-link" target="_blank">SQLAlchemy's `DECIMAL` type</a>.

///

## Decimals in SQLModel

Let's say that each hero in the database will have an amount of money. We could make that field a `Decimal` type using the `condecimal()` function:

//// tab | Python 3.10+

```python hl_lines="11"
{!./docs_src/advanced/decimal/tutorial001_py310.py[ln:1-11]!}

# More code here later 👇
```

////

//// tab | Python 3.7+

```python hl_lines="12"
{!./docs_src/advanced/decimal/tutorial001.py[ln:1-12]!}

# More code here later 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/decimal/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

////

///

Here we are saying that `money` can have at most `5` digits with `max_digits`, **this includes the integers** (to the left of the decimal dot) **and the decimals** (to the right of the decimal dot).

We are also saying that the number of decimal places (to the right of the decimal dot) is `3`, so we can have **3 decimal digits** for these numbers in the `money` field. This means that we will have **2 digits for the integer part** and **3 digits for the decimal part**.

✅ So, for example, these are all valid numbers for the `money` field:

* `12.345`
* `12.3`
* `12`
* `1.2`
* `0.123`
* `0`

🚫 But these are all invalid numbers for that `money` field:

* `1.2345`
  * This number has more than 3 decimal places.
* `123.234`
  * This number has more than 5 digits in total (integer and decimal part).
* `123`
  * Even though this number doesn't have any decimals, we still have 3 places saved for them, which means that we can **only use 2 places** for the **integer part**, and this number has 3 integer digits. So, the allowed number of integer digits is `max_digits` - `decimal_places` = 2.

/// tip

Make sure you adjust the number of digits and decimal places for your own needs, in your own application. 🤓

///

## Create models with Decimals

When creating new models you can actually pass normal (`float`) numbers, Pydantic will automatically convert them to `Decimal` types, and **SQLModel** will store them as `Decimal` types in the database (using SQLAlchemy).

//// tab | Python 3.10+

```Python hl_lines="4-6"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001_py310.py[ln:24-34]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="4-6"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001.py[ln:25-35]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/decimal/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

////

///

## Select Decimal data

Then, when working with Decimal types, you can confirm that they indeed avoid those rounding errors from floats:

//// tab | Python 3.10+

```Python hl_lines="15-16"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001_py310.py[ln:37-50]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="15-16"
# Code above omitted 👆

{!./docs_src/advanced/decimal/tutorial001.py[ln:38-51]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/advanced/decimal/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/advanced/decimal/tutorial001.py!}
```

////

///

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

/// warning

Although Decimal types are supported and used in the Python side, not all databases support it. In particular, SQLite doesn't support decimals, so it will convert them to the same floating `NUMERIC` type it supports.

But decimals are supported by most of the other SQL databases. 🎉

///
