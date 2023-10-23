#!/usr/bin/env bash

set -e
set -x

mypy sqlmodel
ruff sqlmodel tests docs_src scripts
black sqlmodel tests docs_src --check
