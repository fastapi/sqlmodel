#!/usr/bin/env bash

set -e
set -x

mypy sqlmodel
flake8 sqlmodel tests docs_src
black sqlmodel tests docs_src --check
isort sqlmodel tests docs_src scripts --check-only
