# FastAPI Response Model with SQLModel

Now I'll show you how to use FastAPI's `response_model` with **SQLModel**.

## Interactive API Docs

Up to now, with the code we have used, the API docs know the data the clients have to send:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/simple-hero-api/image01.png">

This interactive docs UI is powered by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>, and what Swagger UI does is to read a big JSON content that defines the API with all the data schemas (data shapes) using the standard <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md" class="external-link" target="_blank">OpenAPI</a>, and showing it in that nice <abbr title="User Interface">UI</abbr>.

FastAPI automatically **generates that OpenAPI** for Swagger UI to read it.

And it generates it **based on the code you write**, using the Pydantic models (in this case **SQLModel** models) and type annotations to know the schemas of the data that the API handles.

## Response Data

But up to now, the API docs UI doesn't know the schema of the *responses* our app sends back.

You can see that there's a possible "Successful Response" with a code `200`, but we have no idea how the response data would look like.

<img class="shadow" alt="API docs UI without response data schemas" src="/img/tutorial/fastapi/response-model/image01.png">

Right now, we only tell FastAPI the data we want to receive, but we don't tell it yet the data we want to send back.

Let's do that now. 🤓

## Use `response_model`

We can use `response_model` to tell FastAPI the schema of the data we want to send back.

For example, we can pass the same `Hero` **SQLModel** class (because it is also a Pydantic model):

//// tab | Python 3.10+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/response_model/tutorial001_py310.py[ln:31-37]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/response_model/tutorial001_py39.py[ln:33-39]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/response_model/tutorial001.py[ln:33-39]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001.py!}
```

////

///

## List of Heroes in `response_model`

We can also use other type annotations, the same way we can use with Pydantic fields. For example, we can pass a list of `Hero`s.

First, we import `List` from `typing` and then we declare the `response_model` with `List[Hero]`:

//// tab | Python 3.10+

```Python hl_lines="3"

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/response_model/tutorial001_py310.py[ln:40-44]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/response_model/tutorial001_py39.py[ln:42-46]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="1  5"
{!./docs_src/tutorial/fastapi/response_model/tutorial001.py[ln:1]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/response_model/tutorial001.py[ln:42-46]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/response_model/tutorial001.py!}
```

////

///

## FastAPI and Response Model

FastAPI will do data validation and filtering of the response with this `response_model`.

So this works like a contract between our application and the client.

You can read more about it in the <a href="https://fastapi.tiangolo.com/tutorial/response-model/" class="external-link" target="_blank">FastAPI docs about `response_model`</a>.

## New API Docs UI

Now we can go back to the docs UI and see that they now show the schema of the response we will receive.

<img class="shadow" alt="API docs UI without response data schemas" src="/img/tutorial/fastapi/response-model/image02.png">

The clients will know what data they should expect.

## Automatic Clients

The most visible advantage of using the `response_model` is that it shows up in the API docs UI.

But there are other advantages, like that FastAPI will do automatic <a href="https://fastapi.tiangolo.com/tutorial/response-model/" class="external-link" target="_blank">data validation and filtering</a> of the response data using this model.

Additionally, because the schemas are defined in using a standard, there are many tools that can take advantage of this.

For example, client generators, that can automatically create the code necessary to talk to your API in many languages.

/// info

If you are curious about the standards, FastAPI generates OpenAPI, that internally uses JSON Schema.

You can read about all that in the <a href="https://fastapi.tiangolo.com/tutorial/first-steps/#openapi" class="external-link" target="_blank">FastAPI docs - First Steps</a>.

///

## Recap

Use the `response_model` to tell FastAPI the schema of the data you want to send back and have awesome data APIs. 😎
