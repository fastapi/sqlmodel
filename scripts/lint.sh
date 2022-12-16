#!/usr/bin/env bash

set -e
set -x

mypy sqlmodel
flake8 sqlmodel tests docs_src
black sqlmodel tests docs_src --check
isort sqlmodel tests docs_src scripts --check-only
# TODO: move this to test.sh after deprecating Python 3.6
CHECK_JINJA=1 python scripts/generate_select.py
