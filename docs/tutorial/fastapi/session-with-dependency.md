# Session with FastAPI Dependency

Before we keep adding things, let's change a bit how we get the session for each request to simplify our life later.

## Current Sessions

Up to now, we have been creating a session in each *path operation*, in a `with` block.

//// tab | Python 3.10+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001_py310.py[ln:48-55]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001_py39.py[ln:50-57]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/delete/tutorial001.py[ln:50-57]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/delete/tutorial001.py!}
```

////

///

That's perfectly fine, but in many use cases we would want to use <a href="https://fastapi.tiangolo.com/tutorial/dependencies/" class="external-link" target="_blank">FastAPI Dependencies</a>, for example to **verify** that the client is **logged in** and get the **current user** before executing any other code in the *path operation*.

These dependencies are also very useful during **testing**, because we can **easily replace them**, and then, for example, use a new database for our tests, or put some data before the tests, etc.

So, let's refactor these sessions to use **FastAPI Dependencies**.

## Create a **FastAPI** Dependency

A **FastAPI** dependency is very simple, it's just a function that returns a value.

It could use `yield` instead of `return`, and in that case **FastAPI** will make sure it executes all the code **after** the `yield`, once it is done with the request.

//// tab | Python 3.10+

```Python hl_lines="3-5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:40-42]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:42-44]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-5"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:42-44]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py!}
```

////

///

## Use the Dependency

Now let's make FastAPI execute a dependency and get its value in the *path operation*.

We import `Depends()` from `fastapi`. Then we use it in the *path operation function* in a **parameter**, the same way we declared parameters to get JSON bodies, path parameters, etc.

//// tab | Python 3.10+

```Python hl_lines="1  13"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:1-2]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:40-42]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:53-59]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3  15"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:55-61]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3  15"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:55-61]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py!}
```

////

///

/// tip

Here's a tip about that `*,` thing in the parameters.

Here we are passing the parameter `session` that has a "default value" of `Depends(get_session)` before the parameter `hero`, that doesn't have any default value.

Python would normally complain about that, but we can use the initial "parameter" `*,` to mark all the rest of the parameters as "keyword only", which solves the problem.

You can read more about it in the FastAPI documentation <a href="https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#order-the-parameters-as-you-need-tricks" class="external-link" target="_blank">Path Parameters and Numeric Validations - Order the parameters as you need, tricks</a>

///

The value of a dependency will **only be used for one request**, FastAPI will call it right before calling your code and will give you the value from that dependency.

If it had `yield`, then it will continue the rest of the execution once you are done sending the response. In the case of the **session**, it will finish the cleanup code from the `with` block, closing the session, etc.

Then FastAPI will call it again for the **next request**.

Because it is called **once per request**, we will still get a **single session per request** as we should, so we are still fine with that. ✅

And because dependencies can use `yield`, FastAPI will make sure to run the code **after** the `yield` once it is done, including all the **cleanup code** at the end of the `with` block. So we are also fine with that. ✅

## The `with` Block

This means that in the main code of the *path operation function*, it will work equivalently to the previous version with the explicit `with` block.

//// tab | Python 3.10+

```Python hl_lines="14-18"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:1-2]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:40-42]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:53-59]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="16-20"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:55-61]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="16-20"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:55-61]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py!}
```

////

///

In fact, you could think that all that block of code inside of the `create_hero()` function is still inside a `with` block for the **session**, because this is more or less what's happening behind the scenes.

But now, the `with` block is not explicitly in the function, but in the dependency above:

//// tab | Python 3.10+

```Python hl_lines="7-8"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:1-2]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:40-42]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:53-59]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="9-10"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:55-61]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9-10"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:55-61]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py!}
```

////

///

We will see how this is very useful when testing the code later. ✅

## Update the Path Operations to Use the Dependency

Now we can update the rest of the *path operations* to use the new dependency.

We just declare the dependency in the parameters of the function, with:

```Python
session: Session = Depends(get_session)
```

And then we remove the previous `with` block with the old **session**.

//// tab | Python 3.10+

```Python hl_lines="13  24  33  42  57"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:1-2]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:40-42]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py[ln:53-104]!}
```

////

//// tab | Python 3.9+

```Python hl_lines="15  26  35  44  59"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py[ln:55-106]!}
```

////

//// tab | Python 3.7+

```Python hl_lines="15  26  35  44  59"
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:42-44]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py[ln:55-106]!}
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/session_with_dependency/tutorial001.py!}
```

////

///

## Recap

You just learned how to use **FastAPI dependencies** to handle the database session. This will come in handy later when testing the code.

And you will see how much these dependencies can help the more you work with FastAPI, to handle **permissions**, **authentication**, resources like database **sessions**, etc. 🚀

If you want to learn more about dependencies, checkout the <a href="https://fastapi.tiangolo.com/tutorial/dependencies/" class="external-link" target="_blank">FastAPI docs about Dependencies</a>.
