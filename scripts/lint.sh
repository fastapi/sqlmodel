#!/usr/bin/env bash

set -e
set -x

mypy --no-incremental --show-absolute-path ./sqlmodel
ruff check sqlmodel tests docs_src scripts
ruff format sqlmodel tests docs_src scripts --check
