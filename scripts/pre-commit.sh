#!/bin/bash
# pre-commit.sh - Run type checking and tests before commit

set -e

echo "Running type check..."
uv run mypy src/ --ignore-missing-imports || exit 1
echo "Type check passed."

echo "Running unit tests..."
uv run pytest tests/unit/ -v || exit 1
echo "Unit tests passed."

echo "Running unit tests with coverage..."
uv run pytest tests/unit/ --cov=src --cov-fail-under=30 -q || exit 1
echo "Unit test coverage is above 30%."

echo "Running all tests..."
uv run pytest tests/ -v || exit 1
echo "All tests passed."

echo "Pre-commit checks passed. You may commit now."
