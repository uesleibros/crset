#!/bin/bash
echo "Linting..."
./scripts/lint.sh || exit 1

echo "Type checking..."
mypy app || exit 1

echo "Running tests..."
./scripts/test.sh