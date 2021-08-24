# Read Heroes with Limit and Offset wtih FastAPI

When a client sends a request to get all the heroes, we have been returning them all.

But if we had **thousands** of heroes that could consume a lot of **computational resources**, network bandwith, etc.

So we probably want to limit it.

Let's use the same **offset** and **limit** we learned about in the previous tutorial chapters for the API.

!!! info
    In many cases this is also called **pagination**.

## Add a Limit and Offset to the Query Parameters

Let's add `limit` and `offset` to the query parameters.

By default, we will return the first results from the database, so `offset` will have a default value of `0`.

And by default, we will return a maximum of `100` heroes, so `limit` will have a default value of `100`.

```Python hl_lines="3  9  11"
{!./docs_src/tutorial/fastapi/limit_and_offset/tutorial001.py[ln:1-4]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/limit_and_offset/tutorial001.py[ln:54-58]!}

# Code below omitted 👇
```

<details>
<summary>👀 Full file preview</summary>

```Python
{!./docs_src/tutorial/fastapi/limit_and_offset/tutorial001.py!}
```

</details>

We want to allow clients to set a different `offset` and `limit` values.

But we don't want them to be able to set a `limit` of something like `9999`, that's over `9000`! 😱

So, to prevent it, we add additional validation to the `limit` query parameter, declaring that it has to be **l**ess **t**han or **e**qual to `100` with `lte=100`.

This way, a client can decide to take less heroes if they want, but not more.

!!! info
    If you need to refresh how query parameters and their validation work, check out the docs in FastAPI:

    * <a href="https://fastapi.tiangolo.com/tutorial/query-params/" class="external-link" target="_blank">Query Parameters</a>
    * <a href="https://fastapi.tiangolo.com/tutorial/query-params-str-validations/" class="external-link" target="_blank">Query Parameters and String Validations</a>
    * <a href="https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/" class="external-link" target="_blank">Path Parameters and Numeric Validations</a>

## Check the Docs UI

Now we can see that the docs UI shows the new parameters to control **limit** and **offset** of our data.

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/limit-and-offset/image01.png">

## Recap

You can use **FastAPI**'s automatic data validation to get the parameters for `limit` and `offset`, and then use them with the **session** to control ranges of data to be sent in responses.
