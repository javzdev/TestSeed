#!/usr/bin/env sh
# Run every check that CI runs. Usage: ./scripts/check.sh
set -eu
ruff check .
ruff format --check .
mypy
pytest --cov --cov-report=term-missing
