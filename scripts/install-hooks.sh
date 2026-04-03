#!/usr/bin/env bash
set -euo pipefail

if command -v pnpm >/dev/null 2>&1 && pnpm exec lefthook version >/dev/null 2>&1; then
  pnpm exec lefthook install
else
  echo "lefthook not installed; skipping hook installation"
fi
