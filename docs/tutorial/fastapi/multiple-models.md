# Multiple Models with FastAPI

We have been using the same `Hero` model to declare the schema of the data we receive in the API, the table model in the database, and the schema of the data we send back in responses.

But in most of the cases, there are slight differences. Let's use multiple models to solve it.

Here you will see the main and biggest feature of **SQLModel**. 😎

## Review Creation Schema

Let's start by reviewing the automatically generated schemas from the docs UI.

For input, we have:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/simple-hero-api/image01.png">

If we pay attention, it shows that the client *could* send an `id` in the JSON body of the request.

This means that the client could try to use the same ID that already exists in the database for another hero.

That's not what we want.

We want the client only to send the data that is needed to create a new hero:

* `name`
* `secret_name`
* Optional `age`

And we want the `id` to be generated automatically by the database, so we don't want the client to send it.

We'll see how to fix it in a bit.

## Review Response Schema

Now let's review the schema of the response we send back to the client in the docs UI.

If you click the small tab <kbd>Schema</kbd> instead of the <kbd>Example Value</kbd>, you will see something like this:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/multiple-models/image01.png">

Let's see the details.

The fields with a red asterisk (<span style="color: #ff0000;">*</span>) are "required".

This means that our API application is required to return those fields in the response:

* `name`
* `secret_name`

The `age` is optional, we don't have to return it, or it could be `None` (or `null` in JSON), but the `name` and the `secret_name` are required.

Here's the weird thing, the `id` currently seems also "optional". 🤔

This is because in our **SQLModel** class we declare the `id` with `Optional[int]`, because it could be `None` in memory until we save it in the database and we finally get the actual ID.

But in the responses, we always send a model from the database, so it **always has an ID**. So the `id` in the responses can be declared as required.

This means that our application is making the promise to the clients that if it sends a hero, it will for sure have an `id` with a value, it will not be `None`.

### Why Is it Important to Have a Contract for Responses

The ultimate goal of an API is for some **clients to use it**.

The clients could be a frontend application, a command line program, a graphical user interface, a mobile application, another backend application, etc.

And the code those clients write depends on what our API tells them they **need to send**, and what they can **expect to receive**.

Making both sides very clear will make it much easier to interact with the API.

And in most of the cases, the developer of the client for that API **will also be yourself**, so you are **doing your future self a favor** by declaring those schemas for requests and responses. 😉

### So Why is it Important to Have Required IDs

Now, what's the matter with having one **`id` field marked as "optional"** in a response when in reality it is always required?

For example, **automatically generated clients** in other languages (or also in Python) would have some declaration that this field `id` is optional.

And then the developers using those clients in their languages would have to be checking all the time in all their code if the `id` is not `None` before using it anywhere.

That's a lot of unnecessary checks and **unnecessary code** that could have been saved by declaring the schema properly. 😔

It would be a lot simpler for that code to know that the `id` from a response is required and **will always have a value**.

Let's fix that too. 🤓

## Multiple Hero Schemas

So, we want to have our `Hero` model that declares the **data in the database**:

* `id`, optional on creation, required on database
* `name`, required
* `secret_name`, required
* `age`, optional

But we also want to have a `HeroCreate` for the data we want to receive when **creating** a new hero, which is almost all the same data as `Hero`, except for the `id`, because that is created automatically by the database:

* `name`, required
* `secret_name`, required
* `age`, optional

And we want to have a `HeroPublic` with the `id` field, but this time annotated with `id: int`, instead of `id: Optional[int]`, to make it clear that it is required in responses **read** from the clients:

* `id`, required
* `name`, required
* `secret_name`, required
* `age`, optional

## Multiple Models with Duplicated Fields

The simplest way to solve it could be to create **multiple models**, each one with all the corresponding fields:

//// tab | Python 3.10+

```Python hl_lines="5-9  12-15  18-22"
# This would work, but there's a better option below 🚨

# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py[ln:5-22]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="5-9  12-15  18-22"
# This would work, but there's a better option below 🚨

# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py[ln:7-24]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="5-9  12-15  18-22"
# This would work, but there's a better option below 🚨

# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py[ln:7-24]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py!}
```

////

///

Here's the important detail, and probably the most important feature of **SQLModel**: only `Hero` is declared with `table = True`.

This means that the class `Hero` represents a **table** in the database. It is both a **Pydantic** model and a **SQLAlchemy** model.

But `HeroCreate` and `HeroPublic` don't have `table = True`. They are only **data models**, they are only **Pydantic** models. They won't be used with the database, but only to declare data schemas for the API (or for other uses).

This also means that `SQLModel.metadata.create_all()` won't create tables in the database for `HeroCreate` and `HeroPublic`, because they don't have `table = True`, which is exactly what we want. 🚀

/// tip

We will improve this code to avoid duplicating the fields, but for now we can continue learning with these models.

///

## Use Multiple Models to Create a Hero

Let's now see how to use these new models in the FastAPI application.

Let's first check how is the process to create a hero now:

//// tab | Python 3.10+

```Python hl_lines="3-4  6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py[ln:44-51]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-4  6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py[ln:46-53]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-4  6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py[ln:46-53]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py!}
```

////

///

Let's check that in detail.

Now we use the type annotation `HeroCreate` for the request JSON data in the `hero` parameter of the **path operation function**.

//// tab | Python 3.10+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py[ln:45]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py[ln:47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py[ln:47]!}

# Code below omitted 👇
```

////

Then we create a new `Hero` (this is the actual **table** model that saves things to the database) using `Hero.model_validate()`.

The method `.model_validate()` reads data from another object with attributes (or a dict) and creates a new instance of this class, in this case `Hero`.

In this case, we have a `HeroCreate` instance in the `hero` variable. This is an object with attributes, so we use `.model_validate()` to read those attributes.

/// tip
In versions of **SQLModel** before `0.0.14` you would use the method `.from_orm()`, but it is now deprecated and you should use `.model_validate()` instead.
///

We can now create a new `Hero` instance (the one for the database) and put it in the variable `db_hero` from the data in the `hero` variable that is the `HeroCreate` instance we received from the request.

//// tab | Python 3.10+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py[ln:47]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py[ln:49]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py[ln:49]!}

# Code below omitted 👇
```

////

Then we just `add` it to the **session**, `commit`, and `refresh` it, and finally, we return the same `db_hero` variable that has the just refreshed `Hero` instance.

Because it is just refreshed, it has the `id` field set with a new ID taken from the database.

And now that we return it, FastAPI will validate the data with the `response_model`, which is a `HeroPublic`:

//// tab | Python 3.10+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py310.py[ln:44]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001_py39.py[ln:46]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial001.py[ln:46]!}

# Code below omitted 👇
```

////

This will validate that all the data that we promised is there and will remove any data we didn't declare.

/// tip

This filtering could be very important and could be a very good security feature, for example, to make sure you filter private data, hashed passwords, etc.

You can read more about it in the <a href="https://fastapi.tiangolo.com/tutorial/response-model/" class="external-link" target="_blank">FastAPI docs about Response Model</a>.

///

In particular, it will make sure that the `id` is there and that it is indeed an integer (and not `None`).

## Shared Fields

But looking closely, we could see that these models have a lot of **duplicated information**.

All **the 3 models** declare that they share some **common fields** that look exactly the same:

* `name`, required
* `secret_name`, required
* `age`, optional

And then they declare other fields with some differences (in this case, only about the `id`).

We want to **avoid duplicated information** if possible.

This is important if, for example, in the future, we decide to **refactor the code** and rename one field (column). For example, from `secret_name` to `secret_identity`.

If we have that duplicated in multiple models, we could easily forget to update one of them. But if we **avoid duplication**, there's only one place that would need updating. ✨

Let's now improve that. 🤓

## Multiple Models with Inheritance

And here it is, you found the biggest feature of **SQLModel**. 💎

Each of these models is only a **data model** or both a data model and a **table model**.

So, it's possible to create models with **SQLModel** that don't represent tables in the database.

On top of that, we can use inheritance to avoid duplicated information in these models.

We can see from above that they all share some **base** fields:

* `name`, required
* `secret_name`, required
* `age`, optional

So let's create a **base** model `HeroBase` that the others can inherit from:

//// tab | Python 3.10+

```Python hl_lines="3-6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py[ln:5-8]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="3-6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py[ln:7-10]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="3-6"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py[ln:7-10]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py!}
```

////

///

As you can see, this is *not* a **table model**, it doesn't have the `table = True` config.

But now we can create the **other models inheriting from it**, they will all share these fields, just as if they had them declared.

### The `Hero` **Table Model**

Let's start with the only **table model**, the `Hero`:

//// tab | Python 3.10+

```Python hl_lines="9-10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py[ln:5-12]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="9-10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py[ln:7-14]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="9-10"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py[ln:7-14]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py!}
```

////

///

Notice that `Hero` now doesn't inherit from `SQLModel`, but from `HeroBase`.

And now we only declare one single field directly, the `id`, that here is `Optional[int]`, and is a `primary_key`.

And even though we don't declare the other fields **explicitly**, because they are inherited, they are also part of this `Hero` model.

And of course, all these fields will be in the columns for the resulting `hero` table in the database.

And those inherited fields will also be in the **autocompletion** and **inline errors** in editors, etc.

### Columns and Inheritance with Multiple Models

Notice that the parent model `HeroBase`  is not a **table model**, but still, we can declare `name` and `age` using `Field(index=True)`.

//// tab | Python 3.10+

```Python hl_lines="4  6  9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py[ln:5-12]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="4  6  9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py[ln:7-14]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="4  6  9"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py[ln:7-14]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py!}
```

////

///

This won't affect this parent **data model** `HeroBase`.

But once the child model `Hero` (the actual **table model**) inherits those fields, it will use those field configurations to create the indexes when creating the tables in the database.

### The `HeroCreate` **Data Model**

Now let's see the `HeroCreate` model that will be used to define the data that we want to receive in the API when creating a new hero.

This is a fun one:

//// tab | Python 3.10+

```Python hl_lines="13-14"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py[ln:5-16]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="13-14"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py[ln:7-18]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="13-14"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py[ln:7-18]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py!}
```

////

///

What's happening here?

The fields we need to create are **exactly the same** as the ones in the `HeroBase` model. So we don't have to add anything.

And because we can't leave the empty space when creating a new class, but we don't want to add any field, we just use `pass`.

This means that there's nothing else special in this class apart from the fact that it is named `HeroCreate` and that it inherits from `HeroBase`.

As an alternative, we could use `HeroBase` directly in the API code instead of `HeroCreate`, but it would show up in the automatic docs UI with that name "`HeroBase`" which could be **confusing** for clients. Instead, "`HeroCreate`" is a bit more explicit about what it is for.

On top of that, we could easily decide in the future that we want to receive **more data** when creating a new hero apart from the data in `HeroBase` (for example, a password), and now we already have the class to put those extra fields.

### The `HeroPublic` **Data Model**

Now let's check the `HeroPublic` model.

This one just declares that the `id` field is required when reading a hero from the API, because a hero read from the API will come from the database, and in the database it will always have an ID.

//// tab | Python 3.10+

```Python hl_lines="17-18"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py[ln:5-20]!}

# Code below omitted 👇
```

////

//// tab | Python 3.9+

```Python hl_lines="17-18"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py[ln:7-22]!}

# Code below omitted 👇
```

////

//// tab | Python 3.7+

```Python hl_lines="17-18"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py[ln:7-22]!}

# Code below omitted 👇
```

////

/// details | 👀 Full file preview

//// tab | Python 3.10+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.7+

```Python
{!./docs_src/tutorial/fastapi/multiple_models/tutorial002.py!}
```

////

///

## Review the Updated Docs UI

The FastAPI code is still the same as above, we still use `Hero`, `HeroCreate`, and `HeroPublic`. But now, we define them in a smarter way with inheritance.

So, we can jump to the docs UI right away and see how they look with the updated data.

### Docs UI to Create a Hero

Let's see the new UI for creating a hero:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/multiple-models/image02.png">

Nice! It now shows that to create a hero, we just pass the `name`, `secret_name`, and optionally `age`.

We no longer pass an `id`.

### Docs UI with Hero Responses

Now we can scroll down a bit to see the response schema:

<img class="shadow" alt="Interactive API docs UI" src="/img/tutorial/fastapi/multiple-models/image03.png">

We can now see that `id` is a required field, it has a red asterisk (<span style="color: #f00;">*</span>).

And if we check the schema for the **Read Heroes** *path operation* it will also show the updated schema.

## Inheritance and Table Models

We just saw how powerful the inheritance of these models could be.

This is a very simple example, and it might look a bit... meh. 😅

But now imagine that your table has **10 or 20 columns**. And that you have to duplicate all that information for all your **data models**... then it becomes more obvious why it's quite useful to be able to avoid all that information duplication with inheritance.

Now, this probably looks so flexible that it's not obvious **when to use inheritance** and for what.

Here are a couple of rules of thumb that can help you.

### Only Inherit from Data Models

Only inherit from **data models**, don't inherit from **table models**.

It will help you avoid confusion, and there won't be any reason for you to need to inherit from a **table model**.

If you feel like you need to inherit from a **table model**, then instead create a **base** class that is only a **data model** and has all those fields, like `HeroBase`.

And then inherit from that **base** class that is only a **data model** for any other **data model** and for the **table model**.

### Avoid Duplication - Keep it Simple

It could feel like you need to have a profound reason why to inherit from one model or another, because "in some mystical way" they separate different concepts... or something like that.

In some cases, there are **simple separations** that you can use, like the models to create data, read, update, etc. If that's quick and obvious, nice, use it. 💯

Otherwise, don't worry too much about profound conceptual reasons to separate models, just try to **avoid duplication** and **keep the code simple** enough to reason about it.

If you see you have a lot of **overlap** between two models, then you can probably **avoid some of that duplication** with a base model.

But if to avoid some duplication you end up with a crazy tree of models with inheritance, then it might be **simpler** to just duplicate some of those fields, and that might be easier to reason about and to maintain.

Do whatever is easier to **reason** about, to **program** with, to **maintain**, and to **refactor** in the future. 🤓

Remember that inheritance, the same as **SQLModel**, and anything else, are just tools to **help you be more productive**, that's one of their main objectives. If something is not helping with that (e.g. too much duplication, too much complexity), then change it. 🚀

## Recap

You can use **SQLModel** to declare multiple models:

* Some models can be only **data models**. They will also be **Pydantic** models.
* And some can *also* be **table models** (apart from already being **data models**) by having the config `table = True`. They will also be **Pydantic** models and **SQLAlchemy** models.

Only the **table models** will create tables in the database.

So, you can use all the other **data models** to validate, convert, filter, and document the schema of the data for your application. ✨

You can use inheritance to **avoid information and code duplication**. 😎

And you can use all these models directly with **FastAPI**. 🚀
