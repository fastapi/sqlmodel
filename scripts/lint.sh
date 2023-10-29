#!/usr/bin/env bash

set -e
set -x

mypy sqlmodel
ruff sqlmodel tests docs_src scripts
ruff format sqlmodel tests docs_src --check
