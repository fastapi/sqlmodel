#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place sqlmodel docs_src tests --exclude=__init__.py
black sqlmodel tests docs_src
isort sqlmodel tests docs_src
