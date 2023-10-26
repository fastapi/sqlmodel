#!/bin/sh -e
set -x

ruff sqlmodel tests docs_src scripts --fix
ruff format sqlmodel tests docs_src scripts
