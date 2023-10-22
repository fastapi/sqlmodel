# Contributing

First, you might want to see the basic ways to [help SQLModel and get help](help.md){.internal-link target=_blank}.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.

### Poetry

**SQLModel** uses <a href="https://python-poetry.org/" class="external-link" target="_blank">Poetry</a> to build, package, and publish the project.

You can learn how to install it in the <a href="https://python-poetry.org/docs/#installation" class="external-link" target="_blank">Poetry docs</a>.

After having Poetry available, you can install the development dependencies:

<div class="termy">

```console
$ poetry install

---> 100%
```

</div>

It will also create a virtual environment automatically and will install all the dependencies and your local SQLModel in it.

### Poetry Shell

To use your current environment, and to have access to all the tools in it (for example `pytest` for the tests) enter into a Poetry Shell:

<div class="termy">

```console
$ poetry shell
```

</div>

That will set up the environment variables needed and start a new shell with them.

#### Using your local SQLModel

If you create a Python file that imports and uses SQLModel, and run it with the Python from your local Poetry environment, it will use your local SQLModel source code.

And if you update that local SQLModel source code, when you run that Python file again, it will use the fresh version of SQLModel you just edited.

Poetry takes care of making that work. But of course, it will only work in the current Poetry environment, if you install standard SQLModel in another environment (not from the source in the GitHub repo), that will use the standard SQLModel, not your custom version.

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

## Docs

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a> with <a href="https://squidfunk.github.io/mkdocs-material/" class="external-link" target="_blank">Material for MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

<div class="termy">

```console
$ bash scripts/docs-live.sh

<span style="color: green;">[INFO]</span>    -  Building documentation...
<span style="color: green;">[INFO]</span>    -  Cleaning site directory
<span style="color: green;">[INFO]</span>    -  Documentation built in 2.74 seconds
<span style="color: green;">[INFO]</span>    -  Serving on http://127.0.0.1:8008
```

</div>

It will serve the documentation on `http://127.0.0.1:8008`.

That way, you can edit the documentation/source files and see the changes live.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

## Thanks

Thanks for contributing! ☕
