#!/bin/sh
# Offline unit tests (no network): python3 -m unittest over scripts/tests/
exec python3 -B -m unittest discover -s "$(dirname "$0")/tests" -t "$(dirname "$0")/tests" "$@"
