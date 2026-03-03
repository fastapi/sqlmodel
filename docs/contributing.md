# Contributing

First, you might want to see the basic ways to [help SQLModel and get help](help.md){.internal-link target=_blank}.

## Developing

If you already cloned the <a href="https://github.com/fastapi/sqlmodel" class="external-link" target="_blank">sqlmodel repository</a> and you want to deep dive in the code, here are some guidelines to set up your environment.

### Install Requirements Using `uv`

Create a virtual environment and install the required packages in one command:

<div class="termy">

```console
$ uv sync

---> 100%
```

</div>

It will install all the dependencies and your local SQLModel in your local environment.

### Using your Local SQLModel

If you create a Python file that imports and uses SQLModel, and run it with the Python from your local environment, it will use your cloned local SQLModel source code.

And if you update that local SQLModel source code when you run that Python file again, it will use the fresh version of SQLModel you just edited.

That way, you don't have to "install" your local version to be able to test every change.

/// note | "Technical Details"

This only happens when you install using this included `requirements.txt` instead of running `pip install sqlmodel` directly.

That is because inside the `requirements.txt` file, the local version of SQLModel is marked to be installed in "editable" mode, with the `-e` option.

///

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

### Docs Live

During local development, there is a script that builds the site and checks for any changes, live-reloading:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

It will serve the documentation on `http://127.0.0.1:8008`.

That way, you can edit the documentation/source files and see the changes live.

/// tip

Alternatively, you can perform the same steps that scripts does manually.

Go into the docs director at `docs/`:

```console
$ cd docs/
```

Then run `mkdocs` in that directory:

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer CLI (Optional)

The instructions here show you how to use the script at `./scripts/docs.py` with the `python` program directly.

But you can also use <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, and you will get autocompletion in your terminal for the commands after installing completion.

If you install Typer CLI, you can install completion with:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Docs Structure

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

And there are extra tools/scripts in place in `./scripts/docs.py`.

/// tip

You don't need to see the code in `./scripts/docs.py`, you just use it in the command line.

///

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for Tests

Most of the tests actually run against the example source files in the documentation.

This helps to make sure that:

* The documentation is up-to-date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

## Automated Code and AI

You are encouraged to use all the tools you want to do your work and contribute as efficiently as possible, this includes AI (LLM) tools, etc. Nevertheless, contributions should have meaningful human intervention, judgement, context, etc.

If the **human effort** put in a PR, e.g. writing LLM prompts, is **less** than the **effort we would need to put** to **review it**, please **don't** submit the PR.

Think of it this way: we can already write LLM prompts or run automated tools ourselves, and that would be faster than reviewing external PRs.

### Closing Automated and AI PRs

If we see PRs that seem AI generated or automated in similar ways, we'll flag them and close them.

The same applies to comments and descriptions, please don't copy paste the content generated by an LLM.

### Human Effort Denial of Service

Using automated tools and AI to submit PRs or comments that we have to carefully review and handle would be the equivalent of a <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack" class="external-link" target="_blank">Denial-of-service attack</a> on our human effort.

It would be very little effort from the person submitting the PR (an LLM prompt) that generates a large amount of effort on our side (carefully reviewing code).

Please don't do that.

We'll need to block accounts that spam us with repeated automated PRs or comments.

### Use Tools Wisely

As Uncle Ben said:

<blockquote>
With great <strike>power</strike> <strong>tools</strong> comes great responsibility.
</blockquote>

Avoid inadvertently doing harm.

You have amazing tools at hand, use them wisely to help effectively.
