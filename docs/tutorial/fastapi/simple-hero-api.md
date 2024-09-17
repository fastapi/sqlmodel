# Simple Hero API with FastAPI

Let's start by building a simple hero web API with **FastAPI**. ✨

## Install **FastAPI**

The first step is to install FastAPI.

FastAPI is the framework to create the **web API**.

But we also need another type of program to run it, it is called a "**server**". We will use **Uvicorn** for that. And we will install Uvicorn with its *standard* dependencies.

Then install FastAPI.

Make sure you create a [virtual environment](../../virtual-environments.md){.internal-link target=_blank}, activate it, and then install them, for example with:

<div class="termy">

```console
$ pip install fastapi "uvicorn[standard]"

---> 100%
```

</div>

## **SQLModel** Code - Models, Engine

Now let's start with the SQLModel code.

We will start with the **simplest version**, with just heroes (no teams yet).

This is almost the same code we have seen up to now in previous examples:

//// tab | Python 3.10+

```Python hl_lines="18-19"

# One line of FastAPI imports here later 👈
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:2]!}

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:5-20]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="20-21"
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:1]!}

# One line of FastAPI imports here later 👈
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:4]!}

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:7-22]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py!}
```

////

///

There's only one change here from the code we have used before, the `check_same_thread` in the `connect_args`.

That is a configuration that SQLAlchemy passes to the low-level library in charge of communicating with the database.

`check_same_thread` is by default set to `True`, to prevent misuses in some simple cases.

But here we will make sure we don't share the same **session** in more than one request, and that's the actual **safest way** to prevent any of the problems that configuration is there for.

And we also need to disable it because in **FastAPI** each request could be handled by multiple interacting threads.

/// info

That's enough information for now, you can read more about it in the <a href="https://fastapi.tiangolo.com/async/" class="external-link" target="_blank">FastAPI docs for `async` and `await`</a>.

The main point is, by ensuring you **don't share** the same **session** with more than one request, the code is already safe.

///

## **FastAPI** App

The next step is to create the **FastAPI** app.

We will import the `FastAPI` class from `fastapi`.

And then create an `app` object that is an instance of that `FastAPI` class:

//// tab | Python 3.10+

```Python hl_lines="1  6"
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:1-2]!}

# SQLModel code here omitted 👈

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:23]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  8"
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:1-4]!}

# SQLModel code here omitted 👈

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:25]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py!}
```

////

///

## Create Database and Tables on `startup`

We want to make sure that once the app starts running, the function `create_tables` is called. To create the database and tables.

This should be called only once at startup, not before every request, so we put it in the function to handle the `"startup"` event:

//// tab | Python 3.10+

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:23-28]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="6-8"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:25-30]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py!}
```

////

///

## Create Heroes *Path Operation*

/// info

If you need a refresher on what a **Path Operation** is (an endpoint with a specific HTTP Operation) and how to work with it in FastAPI, check out the <a href="https://fastapi.tiangolo.com/tutorial/first-steps/" class="external-link" target="_blank">FastAPI First Steps docs</a>.

///

Let's create the **path operation** code to create a new hero.

It will be called when a user sends a request with a `POST` **operation** to the `/heroes/` **path**:

//// tab | Python 3.10+

```Python hl_lines="11-12"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:23-37]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="11-12"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:25-39]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py!}
```

////

///

/// info

If you need a refresher on some of those concepts, checkout the FastAPI documentation:

* <a href="https://fastapi.tiangolo.com/tutorial/first-steps/" class="external-link" target="_blank">First Steps</a>
* <a href="https://fastapi.tiangolo.com/tutorial/path-params/" class="external-link" target="_blank">Path Parameters - Data Validation and Data Conversion</a>
* <a href="https://fastapi.tiangolo.com/tutorial/body/" class="external-link" target="_blank">Request Body</a>

///

## The **SQLModel** Advantage

Here's where having our **SQLModel** class models be both **SQLAlchemy** models and **Pydantic** models at the same time shine. ✨

Here we use the **same** class model to define the **request body** that will be received by our API.

Because **FastAPI** is based on Pydantic, it will use the same model (the Pydantic part) to do automatic data validation and <abbr title="also called serialization, marshalling">conversion</abbr> from the JSON request to an object that is an actual instance of the `Hero` class.

And then, because this same **SQLModel** object is not only a **Pydantic** model instance but also a **SQLAlchemy** model instance, we can use it directly in a **session** to create the row in the database.

So we can use intuitive standard Python **type annotations**, and we don't have to duplicate a lot of the code for the database models and the API data models. 🎉

/// tip

We will improve this further later, but for now, it already shows the power of having **SQLModel** classes be both **SQLAlchemy** models and **Pydantic** models at the same time.

///

## Read Heroes *Path Operation*

Now let's add another **path operation** to read all the heroes:

//// tab | Python 3.10+

```Python hl_lines="20-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py[ln:23-44]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="20-24"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py[ln:25-46]!}
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001_py310.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/simple_hero_api/tutorial001.py!}
```

////

///

This is pretty straightforward.

When a client sends a request to the **path** `/heroes/` with a `GET` HTTP **operation**, we run this function that gets the heroes from the database and returns them.

## One Session per Request

Remember that we should use a SQLModel **session** per each group of operations and if we need other unrelated operations we should use a different session?

Here it is much more obvious.

We should normally have **one session per request** in most of the cases.

In some isolated cases, we would want to have new sessions inside, so, **more than one session** per request.

But we would **never want to *share* the same session** among different requests.

In this simple example, we just create the new sessions manually in the **path operation functions**.

In future examples later we will use a <a href="https://fastapi.tiangolo.com/tutorial/dependencies/" class="external-link" target="_blank">FastAPI Dependency</a> to get the **session**, being able to share it with other dependencies and being able to replace it during testing. 🤓

## Run the **FastAPI** Application

Now we are ready to run the FastAPI application.

Put all that code in a file called `main.py`.

Then run it with **Uvicorn**:

<div class="termy">

```console
$ uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

/// info

The command `uvicorn main:app` refers to:

* `main`: the file `main.py` (the Python "module").
* `app`: the object created inside of `main.py` with the line `app = FastAPI()`.

///

### Uvicorn `--reload`

During development (and only during development), you can also add the option `--reload` to Uvicorn.

It will restart the server every time you make a change to the code, this way you will be able to develop faster. 🤓

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Will watch for changes in these directories: ['/home/user/code/sqlmodel-tutorial']
<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

Just remember to never use `--reload` in production, as it consumes much more resources than necessary, would be more error prone, etc.

## Check the API docs UI

Now you can go to that URL in your browser `http://127.0.0.1:8000`. We didn't create a *path operation* for the root path `/`, so that URL alone will only show a "Not Found" error... that "Not Found" error is produced by your FastAPI application.

But you can go to the **automatically generated interactive API documentation** at the path `/docs`: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>. ✨

You will see that this **automatic API docs <abbr title="user interface">UI</abbr>** has the *paths* that we defined above with their *operations*, and that it already knows the shape of the data that the **path operations** will receive:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/simple-hero-api/image01.png">

## Play with the API

You can actually click the button <kbd>Try it out</kbd> and send some requests to create some heroes with the **Create Hero** *path operation*.

And then you can get them back with the **Read Heroes** *path operation*:

<img class="shadow" alt="Interactive API docs UI reading heroes" src="/img/tutorial/fastapi/simple-hero-api/image02.png">

## Check the Database

Now you can terminate that Uvicorn server by going back to the terminal and pressing <kbd>Ctrl+C</kbd>.

And then, you can open **DB Browser for SQLite** and check the database, to explore the data and confirm that it indeed saved the heroes. 🎉

<img class="shadow" alt="DB Browser for SQLite showing the heroes" src="/img/tutorial/fastapi/simple-hero-api/db-browser-01.png">

## Recap

Good job! This is already a FastAPI **web API** application to interact with the heroes database. 🎉

There are several things we can improve and extend. For example, we want the database to decide the ID of each new hero, we don't want to allow a user to send it.

We will make all those improvements in the next chapters. 🚀
