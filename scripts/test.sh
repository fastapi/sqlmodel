#!/usr/bin/env bash

set -e
set -x

CHECK_JINJA=1 python scripts/generate_select.py
coverage run -m pytest tests
coverage combine
coverage report --show-missing
coverage html
