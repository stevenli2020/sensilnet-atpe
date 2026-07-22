#!/bin/bash
set -e

echo "============================================="
echo "  Sensilnet ATPE - Automated Quality Gatekeeper  "
echo "============================================="

# 1. Code Formatting Check
echo "[1/7] Running Ruff linter..."
ruff check src/ tests/

echo "[2/7] Running Black code formatter check..."
black --check src/ tests/

# 2. Type Checking
echo "[3/7] Running Mypy type checker..."
mypy src/

# 3. Unit & Integration Testing
echo "[4/7] Running Pytest suite & Coverage..."
pytest --cov=src tests/ --cov-fail-under=80

# 4. Dependency Integrity
echo "[5/7] Verifying package dependencies..."
pip check

# 5. Leftover Debug Code Scan
echo "[6/7] Checking for leftover debug code (TODO, FIXME, print statements)..."
if grep -rnw 'src/' -e 'TODO' -e 'FIXME' -e 'print('; then
    echo "ERROR: Leftover debug code or print statements detected in src/!"
    exit 1
fi

# 6. Uncommitted Changes Check
echo "[7/7] Checking Git workspace status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "WARNING: Uncommitted changes present in workspace."
fi

echo "============================================="
echo "  SUCCESS: All Quality Gate Checks Passed!   "
echo "============================================="
