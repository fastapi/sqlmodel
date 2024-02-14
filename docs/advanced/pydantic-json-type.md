# Storing Pydantic models at database

In some cases you might need to be able to store Pydantic models as a JSON data instead of create new table for them. You can do it now with new SqlAlchemy type `PydanticJSonType` mapped to BaseModel inside SqlModel.

For example let's add some stats to our heroes and save them at database as JSON data.

At first, we need to create new class `Stats` inherited from pydantic `BaseModel` or even `SqlModel`:

```{.python .annotate  }
{!./docs_src/advanced/pydantic_json_type/tutorial001.py[ln:8-14]!}
```

Then create new field `stats` to `Hero` model

```{.python .annotate  hl_lines="6" }
{!./docs_src/advanced/pydantic_json_type/tutorial001.py[ln:17-22]!}
```
And... that's all of you need to do to store pydantic data as JSON at database.

/// details | 👀 Full tutorial preview
```Python
{!./docs_src/advanced/pydantic_json_type/tutorial001.py!}
```

///

Here we define new Pydantic model `Stats` contains statistics of our hero and map this model to SqlModel class `Hero`.

Then we create new instances of Hero model with random generated stats and save it at database.


# How to watch for mapped model changes at runtime

In previous example we have one *non bug but feature* - `Stats` model isn't mutable and if we try to load our Hero form database and  then change some stats and call `session.commit()` there no changes will be saved.

Let's see how to avoid it.

At first, we need to inherit our Stats model from `sqlalchemy.ext.mutable.Mutable`:
```{.python .annotate hl_lines="1" }
{!./docs_src/advanced/pydantic_json_type/tutorial002.py[ln:10-19]!}
```

Then map Stats to Hero as shown bellow:
```{.python .annotate hl_lines="1-4" }
{!./docs_src/advanced/pydantic_json_type/tutorial002.py[ln:36-39]!}
```

After all of these actions we can change mutated model, and it will be saved to database after we call `session.commit()`

```{.python .annotate hl_lines="4" }
{!./docs_src/advanced/pydantic_json_type/tutorial002.py[ln:76-94]!}
```

/// details | 👀 Full tutorial preview

```Python
{!./docs_src/advanced/pydantic_json_type/tutorial002.py!}
```

///
