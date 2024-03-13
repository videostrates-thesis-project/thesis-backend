#!/bin/bash

echo "[INFO] Running linting tools"
source tools/lint.sh

echo "[INFO] Running tests"
pytest -v --cov-config .coveragerc --cov=src -l --tb=short --maxfail=1 tests/

echo "[INFO] Exporting coverage"
coverage xml
coverage html

echo "[INFO] Done testing"
