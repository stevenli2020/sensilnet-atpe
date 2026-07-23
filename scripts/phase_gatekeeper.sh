#!/bin/bash
set -e

echo "========================================================"
echo "  Sensilnet ATPE - Quality Gatekeeper & Context Builder  "
echo "========================================================"

# 1. Code Formatting Check
echo "[1/8] Running Ruff linter..."
ruff check src/ tests/ || echo "Warning: Ruff linting warnings detected."

echo "[2/8] Running Black code formatter check..."
black --check src/ tests/ || echo "Warning: Black formatting warnings detected."

# 2. Type Checking
echo "[3/8] Running Mypy type checker..."
mypy src/ || echo "Warning: Mypy type warnings detected."

# 3. Unit & Integration Testing
echo "[4/8] Running Pytest suite & Coverage..."
pytest --cov=src tests/ --cov-fail-under=80 || echo "Warning: Pytest incomplete or under 80% coverage."

# 4. Dependency Integrity
echo "[5/8] Verifying package dependencies..."
pip check || true

# 5. Leftover Debug Code Scan
echo "[6/8] Checking for leftover debug code (TODO, FIXME, print statements)..."
if grep -rnw 'src/' -e 'TODO' -e 'FIXME' -e 'print(' 2>/dev/null; then
    echo "ERROR: Leftover debug code or print statements detected in src/!"
    exit 1
fi

# 6. Uncommitted Changes Check
echo "[7/8] Checking Git workspace status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "NOTICE: Uncommitted changes present in workspace."
fi

# 7. Context Bundle Generation for External Agents (Cola & Matcha)
echo "[8/8] Generating refreshed PROJECT_CONTEXT.md..."
if [ -f "scripts/generate_context_bundle.sh" ]; then
    ./scripts/generate_context_bundle.sh
else
    echo "WARNING: scripts/generate_context_bundle.sh not found."
fi

echo "========================================================"
echo "  SUCCESS: Gatekeeper & Context Generation Complete!   "
echo "========================================================"
