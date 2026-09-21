#!/usr/bin/env bash

set -e
set -x

ty check sqlmodel tests/test_field_sa_type.py tests/test_select_typing.py
ruff check sqlmodel tests docs_src scripts
ruff format sqlmodel tests docs_src scripts --check
