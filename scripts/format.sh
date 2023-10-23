#!/bin/sh -e
set -x

ruff sqlmodel tests docs_src scripts --fix
black sqlmodel tests docs_src scripts
