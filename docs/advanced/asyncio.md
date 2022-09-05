# Asyncio Session and Engine

In some cases, you may use asynchronous session and engine.
This is especially important if you are building a highly loaded service.

The advantage of asynchronous over synchronous is that our application does 
not wait for a response from a query to the database, 
but performs other tasks until it receives a response.

To use the asynchronous mode, we need to install the asynchronous driver.

There is aiosqlite driver for sqlite.

<div class="termy">

```console
$ pip install aiosqlite
---> 100%
Successfully installed aiosqlite
```

</div>


Next, you can import the asyncio module, or use the async framework.
In this case, we will use the asyncio library.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:1]!}
```

Importing the asynchronous session and engine.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:4]!}
```

Create Model Hero.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:7-11]!}
```

Setting engine.

Pay attention to the connection url,
it clearly specifies which driver to use to connect to the database.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:14-17]!}
```

Create table database.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:20-22]!}
```

Create rows.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:25-37]!}
```

Read rows. Using the asynchronous context manager.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:40-45]!}
```

We connect all the functions together.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:48-51]!}
```

Running an asynchronous function (python3.7+)

```Python
{!./docs_src/advanced/asyncio/tutorial001.py[ln:53-55]!}
```

Running an asynchronous function (python3.6)

```Python
{!./docs_src/advanced/asyncio/tutorial001_py36.py[ln:53-56]!}
```

Full example.

```Python
{!./docs_src/advanced/asyncio/tutorial001.py!}
```