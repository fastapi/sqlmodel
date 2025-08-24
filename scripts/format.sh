#!/usr/bin/env bash

set -e
set -x

ruff check sqlmodel tests docs_src scripts --fix
ruff format sqlmodel tests docs_src scripts
