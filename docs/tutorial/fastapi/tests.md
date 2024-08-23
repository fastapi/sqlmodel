# Test Applications with FastAPI and SQLModel

To finish this group of chapters about **FastAPI** with **SQLModel**, let's now learn how to implement automated tests for an application using FastAPI with SQLModel. ✅

Including the tips and tricks. 🎁

## FastAPI Application

Let's work with one of the **simpler** FastAPI applications we built in the previous chapters.

All the same **concepts**, **tips** and **tricks** will apply to more complex applications as well.

We will use the application with the hero models, but without team models, and we will use the dependency to get a **session**.

Now we will see how useful it is to have this session dependency. ✨

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/main.py!}
```

///

## File Structure

Now we will have a Python project with multiple files, one file `main.py` with all the application, and one file `test_main.py` with the tests, with the same ideas from [Code Structure and Multiple Files](../code-structure.md){.internal-link target=_blank}.

The file structure is:

```
.
├── project
    ├── __init__.py
    ├── main.py
    └── test_main.py
```

## Testing FastAPI Applications

If you haven't done testing in FastAPI applications, first check the <a href="https://fastapi.tiangolo.com/tutorial/testing/" class="external-link" target="_blank">FastAPI docs about Testing</a>.

Then, we can continue here, the first step is to install the dependencies, `requests` and `pytest`.

Make sure you create a [virtual environment](../../virtual-environments.md){.internal-link target=_blank}, activate it, and then install them, for example with:

<div class="termy">

```console
$ pip install requests pytest

---> 100%
```

</div>

## Basic Tests Code

Let's start with a simple test, with just the basic test code we need the check that the **FastAPI** application is creating a new hero correctly.

```{ .python .annotate }
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_001.py[ln:1-7]!}
        # Some code here omitted, we will see it later 👈
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_001.py[ln:20-24]!}
        # Some code here omitted, we will see it later 👈
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_001.py[ln:26-32]!}

# Code below omitted 👇
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_001.md!}

/// tip

Check out the number bubbles to see what is done by each line of code.

///

That's the **core** of the code we need for all the tests later.

But now, we need to deal with a bit of logistics and details we are not paying attention to just yet. 🤓

## Testing Database

This test looks fine, but there's a problem.

If we run it, it will use the same **production database** that we are using to store our very important **heroes**, and we will end up adding unnecessary data to it, or even worse, in future tests we could end up removing production data.

So, we should use an independent **testing database**, just for the tests.

To do this, we need to change the URL used for the database.

But when the code for the API is executed, it gets a **session** that is already connected to an **engine**, and the **engine** is already using a specific database URL.

Even if we import the variable from the `main` module and change its value just for the tests, by that point the **engine** is already created with the original value.

But all our API *path operations* get the *session* using a FastAPI **dependency**, and we can override dependencies in tests.

Here's where dependencies start to help a lot.

## Override a Dependency

Let's override the `get_session()` dependency for the tests.

This dependency is used by all the *path operations* to get the **SQLModel** session object.

We will override it to use a different **session** object just for the tests.

That way we protect the production database and we have better control of the data we are testing.

```{ .python .annotate hl_lines="4  9-10  12  19" }
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_002.py[ln:1-7]!}
        # Some code here omitted, we will see it later 👈
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_002.py[ln:15-32]!}

# Code below omitted 👇
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_002.md!}

/// tip

Check out the number bubbles to see what is done by each line of code.

///

## Create the Engine and Session for Testing

Now let's create that **session** object that will be used during testing.

It will use its own **engine**, and this new engine will use a new URL for the testing database:

```
sqlite:///testing.db
```

So, the testing database will be in the file `testing.db`.

``` { .python .annotate hl_lines="4  8-11  13  16  33"}
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_003.py!}
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_003.md!}

### Import Table Models

Here we create all the tables in the testing database with:

```Python
SQLModel.metadata.create_all(engine)
```

But remember that [Order Matters](../create-db-and-table.md#sqlmodel-metadata-order-matters){.internal-link target=_blank} and we need to make sure all the **SQLModel** models are already defined and **imported** before calling `.create_all()`.

In this case, it all works for a little subtlety that deserves some attention.

Because we import something, *anything*, from `.main`, the code in `.main` will be executed, including the definition of the **table models**, and that will automatically register them in `SQLModel.metadata`.

That way, when we call `.create_all()` all the **table models** are correctly registered in `SQLModel.metadata` and it will all work. 👌

## Memory Database

Now we are not using the production database. Instead, we use a **new testing database** with the `testing.db` file, which is great.

But SQLite also supports having an **in memory** database. This means that all the database is only in memory, and it is never saved in a file on disk.

After the program terminates, **the in-memory database is deleted**, so it wouldn't help much for a production database.

But **it works great for testing**, because it can be quickly created before each test, and quickly removed after each test. ✅

And also, because it never has to write anything to a file and it's all just in memory, it will be even faster than normally. 🏎

/// details | Other alternatives and ideas 👀

Before arriving at the idea of using an **in-memory database** we could have explored other alternatives and ideas.

The first is that we are not deleting the file after we finish the test, so the next test could have **leftover data**. So, the right thing would be to delete the file right after finishing the test. 🔥

But if each test has to create a new file and then delete it afterwards, running all the tests could be **a bit slow**.

Right now, we have a file `testing.db` that is used by all the tests (we only have one test now, but we will have more).

So, if we tried to run the tests at the same time **in parallel** to try to speed things up a bit, they would clash trying to use the *same* `testing.db` file.

Of course, we could also fix that, using some **random name** for each testing database file... but in the case of SQLite, we have an even better alternative by just using an **in-memory database**. ✨

///

## Configure the In-Memory Database

Let's update our code to use the in-memory database.

We just have to change a couple of parameters in the **engine**.

```{ .python .annotate hl_lines="3  9-13"}
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_004.py[ln:1-13]!}

# Code below omitted 👇
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_004.md!}

/// tip

Check out the number bubbles to see what is done by each line of code.

///

That's it, now the test will run using the **in-memory database**, which will be faster and probably safer.

And all the other tests can do the same.

## Boilerplate Code

Great, that works, and you could replicate all that process in each of the test functions.

But we had to add a lot of **boilerplate code** to handle the custom database, creating it in memory, the custom session, and the dependency override.

Do we really have to duplicate all that for **each test**? No, we can do better! 😎

We are using **pytest** to run the tests. And pytest also has a very similar concept to the **dependencies in FastAPI**.

/// info

In fact, pytest was one of the things that inspired the design of the dependencies in FastAPI.

///

It's a way for us to declare some **code that should be run before** each test and **provide a value** for the test function (that's pretty much the same as FastAPI dependencies).

In fact, it also has the same trick of allowing to use `yield` instead of `return` to provide the value, and then **pytest** makes sure that the code after `yield` is executed *after* the function with the test is done.

In pytest, these things are called **fixtures** instead of *dependencies*.

Let's use these **fixtures** to improve our code and reduce de duplicated boilerplate for the next tests.

## Pytest Fixtures

You can read more about them in the <a href="https://docs.pytest.org/en/6.2.x/fixture.html" class="external-link" target="_blank">pytest docs for fixtures</a>, but I'll give you a short example for what we need here.

Let's see the first code example with a fixture:

``` { .python .annotate }
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_005.py!}
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_005.md!}

/// tip

Check out the number bubbles to see what is done by each line of code.

///

**pytest** fixtures work in a very similar way to FastAPI dependencies, but have some minor differences:

* In pytest fixtures, we need to add a decorator of `@pytest.fixture()` on top.
* To use a pytest fixture in a function, we have to declare the parameter with the **exact same name**. In FastAPI we have to **explicitly use `Depends()`** with the actual function inside it.

But apart from the way we declare them and how we tell the framework that we want to have them in the function, they **work in a very similar way**.

Now we create lot's of tests and re-use that same fixture in all of them, saving us that **boilerplate code**.

**pytest** will make sure to run them right before (and finish them right after) each test function. So, each test function will actually have its own database, engine, and session.

## Client Fixture

Awesome, that fixture helps us prevent a lot of duplicated code.

But currently, we still have to write some code in the test function that will be repetitive for other tests, right now we:

* create the **dependency override**
* put it in the `app.dependency_overrides`
* create the `TestClient`
* Clear the dependency override(s) after making the request

That's still gonna be repetitive in the other future tests. Can we improve it? Yes! 🎉

Each **pytest** fixture (the same way as **FastAPI** dependencies), can require other fixtures.

So, we can create a **client fixture** that will be used in all the tests, and it will itself require the **session fixture**.

``` { .python .annotate hl_lines="19-28  31" }
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main_006.py!}
```

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/annotations/en/test_main_006.md!}

/// tip

Check out the number bubbles to see what is done by each line of code.

///

Now we have a **client fixture** that, in turn, uses the **session fixture**.

And in the actual test function, we just have to declare that we require this **client fixture**.

## Add More Tests

At this point, it all might seem like we just did a lot of changes for nothing, to get **the same result**. 🤔

But normally we will create **lots of other test functions**. And now all the boilerplate and complexity is **written only once**, in those two fixtures.

Let's add some more tests:

```Python hl_lines="3  22"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py[ln:30-58]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py!}
```

///

/// tip

It's always **good idea** to not only test the normal case, but also that **invalid data**, **errors**, and **corner cases** are handled correctly.

That's why we add these two extra tests here.

///

Now, any additional test functions can be as **simple** as the first one, they just have to **declare the `client` parameter** to get the `TestClient` **fixture** with all the database stuff setup. Nice! 😎

## Why Two Fixtures

Now, seeing the code, we could think, why do we put **two fixtures** instead of **just one** with all the code? And that makes total sense!

For these examples, **that would have been simpler**, there's no need to separate that code into two fixtures for them...

But for the next test function, we will require **both fixtures**, the **client** and the **session**.

```Python hl_lines="6  10"
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py[ln:1-6]!}

# Code here omitted 👈

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py[ln:61-81]!}

# Code below omitted 👇
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py!}
```

///

In this test function, we want to check that the *path operation* to **read a list of heroes** actually sends us heroes.

But if the **database is empty**, we would get an **empty list**, and we wouldn't know if the hero data is being sent correctly or not.

But we can **create some heroes** in the testing database right before sending the API request. ✨

And because we are using the **testing database**, we don't affect anything by creating heroes for the test.

To do it, we have to:

* import the `Hero` model
* require both fixtures, the **client** and the **session**
* create some heroes and save them in the database using the **session**

After that, we can send the request and check that we actually got the data back correctly from the database. 💯

Here's the important detail to notice: we can require fixtures in other fixtures **and also** in the test functions.

The function for the **client fixture** and the actual testing function will **both** receive the same **session**.

## Add the Rest of the Tests

Using the same ideas, requiring the fixtures, creating data that we need for the tests, etc., we can now add the rest of the tests. They look quite similar to what we have done up to now.

```Python hl_lines="3  18  33"
# Code above omitted 👆

{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py[ln:84-125]!}
```

/// details | 👀 Full file preview

```Python
{!./docs_src/tutorial/fastapi/app_testing/tutorial001/test_main.py!}
```

///

## Run the Tests

Now we can run the tests with `pytest` and see the results:

<div class="termy">

```console
$ pytest

============= test session starts ==============
platform linux -- Python 3.7.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/user/code/sqlmodel-tutorial
<b>collected 7 items                              </b>

---> 100%

project/test_main.py <font color="#A6E22E">.......         [100%]</font>

<font color="#A6E22E">============== </font><font color="#A6E22E"><b>7 passed</b></font><font color="#A6E22E"> in 0.83s ===============</font>
```

</div>

## Recap

Did you read all that? Wow, I'm impressed! 😎

Adding tests to your application will give you a lot of **certainty** that everything is **working correctly**, as you intended.

And tests will be notoriously useful when **refactoring** your code, **changing things**, **adding features**. Because tests can help catch a lot of errors that can be easily introduced by refactoring.

And they will give you the confidence to work faster and **more efficiently**, because you know that you are checking if you are **not breaking anything**. 😅

I think tests are one of those things that bring your code and you as a developer to the next professional level. 😎

And if you read and studied all this, you already know a lot of the advanced ideas and tricks that took me years to learn. 🚀
