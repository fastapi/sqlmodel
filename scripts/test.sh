#!/usr/bin/env bash

set -e
set -x

coverage run --source=sqlmodel -m pytest tests/
coverage combine
coverage report --show-missing
coverage html --title="SQLModel Coverage"