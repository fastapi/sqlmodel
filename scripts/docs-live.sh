#!/usr/bin/env bash

set -e

export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib"

mkdocs serve --dev-addr 127.0.0.1:8008
