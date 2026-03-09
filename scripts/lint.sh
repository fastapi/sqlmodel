#!/usr/bin/env bash

set -e
set -x

mypy sqlmodel
mypy tests/test_select_typing.py
ty check sqlmodel
ruff check sqlmodel tests docs_src scripts
ruff format sqlmodel tests docs_src scripts --check
