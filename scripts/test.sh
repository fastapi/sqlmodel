#!/usr/bin/env bash

set -e
set -x

coverage run -m pytest tests
coverage combine
coverage report
coverage html
