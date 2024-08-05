# Features

## Designed for **FastAPI**

**SQLModel** was created by the same <a href="https://tiangolo.com/" class="external-link" target="_blank">author</a> of FastAPI.

<a href="https://fastapi.tiangolo.com" target="_blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" style="width: 20%;"></a>

It follows the same design and ideas, and it was created to be the most intuitive way to interact with SQL databases in FastAPI applications.

Nevertheless, SQLModel is completely **independent** of FastAPI and can be used with any other type of application. You can still benefit from its features.

## Just Modern Python

It's all based on standard <abbr title="Currently supported versions of Python">modern **Python**</abbr> type annotations. No new syntax to learn. Just standard modern Python.

If you need a 2 minute refresher of how to use Python types (even if you don't use SQLModel or FastAPI), check the FastAPI tutorial section: <a href="https://fastapi.tiangolo.com/python-types/" class="external-link" target="_blank">Python types intro</a>.

You will also see a 20 seconds refresher on the section [Tutorial - User Guide: First Steps](tutorial/index.md){.internal-link target=_blank}.

## Editor support

**SQLModel** was designed to be easy and intuitive to use to ensure the best development experience, with autocompletion everywhere.

Here's how your editor might help you:

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

<img class="shadow" src="/img/index/autocompletion02.png">

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

<img class="shadow" src="/img/features/autocompletion01.png">

You will get completion for everything while writing the **minimum** amount of code.

You won't need to keep guessing the types of different attributes in your models, if they could be `None`, etc. Your editor will be able to help you with everything because **SQLModel** is based on **standard Python type annotations**.

**SQLModel** adopts <a href="https://peps.python.org/pep-0681/" class="external-link" target="_blank">PEP 681</a> for Python type annotations to ensure the **best developer experience**, so you will get inline errors and autocompletion even while creating new model instances.

<img class="shadow" src="/img/index/autocompletion01.png">

## Short

**SQLModel** has **sensible defaults** for everything, with **optional configurations** everywhere.

But by default, it all **"just works"**.

You can start with the simplest (and most intuitive) type annotations for your data.

And later, you can fine-tune everything with all the power of SQLAlchemy and Pydantic.

## Based on Pydantic

**SQLModel** is based on Pydantic and keeps the same design, syntax, and ideas.

Underneath, ✨ a **SQLModel** model is also a **Pydantic** model. ✨

There was a lot of research and effort dedicated to make it that way.

That means you get all of **Pydantic's features**, including automatic data **validation**, **serialization**, and **documentation**. You can use SQLModel in the same way you can use Pydantic.

You can even create SQLModel models that do *not* represent SQL tables. In that case, they would be **the same as Pydantic models**.

This is useful, in particular, because now you can create a SQL database model that *inherits* from another non-SQL model. You can use that to **reduce code duplication** a lot. It will also make your code more consistent, improve editor support, etc.

This makes it the perfect combination for working with SQL databases in **FastAPI** applications. 🚀

You will learn more about combining different models later in the tutorial.

## Based on SQLAlchemy

**SQLModel** is also based on SQLAlchemy and uses it for everything.

Underneath, ✨ a **SQLModel** model is also a **SQLAlchemy** model. ✨

There was **a lot** of research and effort dedicated to make it that way. In particular, there was a lot of effort and experimentation in making a single model be **both a SQLAlchemy model and a Pydantic** model at the same time.

That means that you get all the power, robustness, and certainty of SQLAlchemy, the <a href="https://lp.jetbrains.com/python-developers-survey-2022/" class="external-link" target="_blank">most widely used database library in Python</a>.

**SQLModel** provides its own utilities to <abbr title="with type completion, type checks, etc.">improve the developer experience</abbr>, but underneath, it uses all of SQLAlchemy.

You can even **combine** SQLModel models with SQLAlchemy models.

SQLModel is designed to satisfy the **most common use cases** and to be as simple and convenient as possible for those cases, providing the best developer experience.

But when you have more exotic use cases that require more complex features, you can still plug SQLAlchemy directly into SQLModel and use all its features in your code.

## Tested

* 100% <abbr title="The amount of code that is automatically tested">test coverage</abbr> (currently 97%, reaching 100% in the coming days/weeks).
* 100% <abbr title="Python type annotations, with this your editor and external tools can give you better support">type annotated</abbr> code base.
