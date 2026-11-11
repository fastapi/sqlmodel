# FastAPI and Pydantic - Intro

One of the use cases where **SQLModel** shines the most, and the main one why it was built, was to be combined with **FastAPI**. ✨

[FastAPI](https://fastapi.tiangolo.com/) is a Python web framework for building web APIs created by the same [author](https://twitter.com/tiangolo) of SQLModel. FastAPI is also built on top of **Pydantic**.

In this group of chapters we will see how to combine SQLModel **table models** representing tables in the SQL database as all the ones we have seen up to now, with **data models** that only represent data (which are actually just Pydantic models behind the scenes).

Being able to combine SQLModel **table** models with pure **data** models would be useful on its own, but to make all the examples more concrete, we will use them with **FastAPI**.

By the end we will have a **simple** but **complete** web **API** to interact with the data in the database. 🎉

## Learning FastAPI

If you have never used FastAPI, maybe a good idea would be to go and study it a bit before continuing.

Just reading and trying the examples on the [FastAPI main page](https://fastapi.tiangolo.com/) should be enough, and it shouldn't take you more than **10 minutes**.
