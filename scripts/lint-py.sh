#!/usr/bin/env bash
set -euo pipefail

if python3 -m ruff --version >/dev/null 2>&1; then
  python3 -m ruff check scripts
else
  echo "ruff not installed; skipping Python lint"
fi
