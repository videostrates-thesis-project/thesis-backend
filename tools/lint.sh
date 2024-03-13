#!/bin/bash

echo "[INFO] Running linting tools"

echo "[INFO] Running isort"
isort src

echo "[INFO] Running flake8"
flake8 src/

echo "[INFO] Running black on src/"
black -l 79 src/

echo "[INFO] Running black on tests/"
black -l 79 tests/

echo "[INFO] Installing mypy types"
mypy --install-types < yes

echo "[INFO] Running mypy"
mypy src/

echo "[INFO] Done linting"
