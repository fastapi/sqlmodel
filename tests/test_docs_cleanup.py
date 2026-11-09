from pathlib import Path

import pytest

from scripts.docs import remove_unused_docs_src


def create_files(paths: set[str]) -> None:
    for path_str in paths:
        path = Path(path_str)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Example code\n", encoding="utf-8")


def include_file(path: str) -> None:
    doc = Path("docs/en/docs/tutorial.md")
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("{* " + path + " *}\n", encoding="utf-8")


@pytest.mark.parametrize(
    "names",
    [
        ("tutorial001", "tutorial001_non_an"),
        ("tutorial001", "tutorial001_an"),
        ("tutorial001_py310", "tutorial001_non_an_py310"),
        ("tutorial001_py310", "tutorial001_an_py310"),
        (
            "tutorial001_py310",
            "tutorial001_an_py310",
            "tutorial001_py314",
            "tutorial001_an_py314",
        ),
        (
            "tutorial001_py311",
            "tutorial001_non_an_py311",
            "tutorial001_py314",
            "tutorial001_non_an_py314",
        ),
        ("tutorial001_py311", "tutorial001_py314"),
        ("tutorial_another", "tutorial_another_non_an"),
    ],
)
@pytest.mark.parametrize("preferred", [0, 1])
def test_keep_file_variants(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    names: tuple[str, ...],
    preferred: int,
) -> None:
    monkeypatch.chdir(tmp_path)
    kept = {f"docs_src/tutorial/topic/{name}.py" for name in names}
    unused = {
        "docs_src/tutorial/topic/tutorial002.py",
        "docs_src/tutorial/topic/tutorial001_extra.py",
    }
    create_files(kept | unused)
    include_file(f"docs_src/tutorial/topic/{names[preferred]}.py")

    remove_unused_docs_src()

    assert {path.as_posix() for path in Path("docs_src").rglob("*.py")} == kept


@pytest.mark.parametrize(
    "names",
    [
        ("tutorial001", "tutorial001_non_an"),
        ("tutorial001", "tutorial001_an"),
        (
            "tutorial001_py310",
            "tutorial001_an_py310",
            "tutorial001_py314",
            "tutorial001_an_py314",
        ),
        (
            "tutorial001_py311",
            "tutorial001_non_an_py311",
            "tutorial001_py314",
            "tutorial001_non_an_py314",
        ),
    ],
)
@pytest.mark.parametrize("preferred", [0, 1])
@pytest.mark.parametrize("included", ["main.py", "routers/items.py", "__init__.py"])
@pytest.mark.parametrize(
    "topic", ["tutorial/code_structure", "tutorial/fastapi/app_testing"]
)
def test_keep_entire_variant_packages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    names: tuple[str, ...],
    preferred: int,
    included: str,
    topic: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    kept = {
        f"docs_src/{topic}/{name}/{module}"
        for name in names
        for module in (
            "__init__.py",
            "main.py",
            "config.py",
            "routers/items.py",
            "routers/utils.py",
            "empty_package/__init__.py",
        )
    }
    kept.add(f"docs_src/{topic}/{names[1]}/variant_only.py")
    unused = {
        f"docs_src/{topic}/tutorial002/main.py",
        f"docs_src/{topic}/tutorial002/__init__.py",
        f"docs_src/{topic}/tutorial002/empty_package/__init__.py",
        f"docs_src/{topic}/tutorial002/routers/items.py",
    }
    create_files(kept | unused)
    include_file(f"docs_src/{topic}/{names[preferred]}/{included}")

    remove_unused_docs_src()

    assert {path.as_posix() for path in Path("docs_src").rglob("*.py")} == kept
    assert not Path(f"docs_src/{topic}/tutorial002").exists()
