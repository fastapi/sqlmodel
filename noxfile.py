from pathlib import Path
from textwrap import dedent

from nox import parametrize
from nox_poetry import Session, session

pydantic1 = ">=1.10.0,<2.0.0"
pydantic2 = ">=2.0.2,<3.0.0"
pydantic_versions = {
    pydantic1: "pyd1",
    pydantic2: "pyd2",
}


@session(python=["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
@parametrize("pydantic", list(pydantic_versions.keys()), ids=pydantic_versions.values())
def tests(session: Session, pydantic: str) -> None:
    """Run pytest with coverage."""
    session.run_always("poetry", "install", external=True)
    session.install(".")
    session.run_always(
        "pip", "install", "--upgrade", f"pydantic{pydantic}", external=True
    )
    my_env = {
        # Need to set PYTHONPATH because some tests depend on docs_src
        "PYTHONPATH": session.invoked_from,
        "COVERAGE_FILE": f"coverage/.coverage.py{session.python}-{pydantic_versions[pydantic]}",
        "CONTEXT": f"py{session.python}-{pydantic_versions[pydantic]}",
    }
    session.log(f"Using env: {my_env}")
    session.run("bash", "scripts/test.sh", env=my_env, external=True)
    session.notify("coverage")


@session(python=["3.8"])
def coverage(session: Session) -> None:
    """Gather coverage from test runs."""
    session.install("coverage[toml]", ".")
    session.run("coverage", "combine", "coverage")
    session.run("coverage", "report")
    session.run("coverage", "html", "--show-contexts", "--title", "Coverage")


@session
@parametrize("python", ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"])
@parametrize("pydantic", list(pydantic_versions.keys()), ids=pydantic_versions.values())
def lint(session: Session, python: str, pydantic: str) -> None:
    """Run lint checks."""
    if python != "3.7" and pydantic == pydantic2:
        session.run_always("poetry", "install", external=True)
        session.install(".")
        session.run_always(
            "pip", "install", "--upgrade", f"pydantic{pydantic}", external=True
        )
        session.run("bash", "scripts/lint.sh", external=True)


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    if session.bin is None:
        return

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))


@session(name="pre-commit", python="3.12")
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install("ruff", "pre-commit", "pre-commit-hooks")
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)
