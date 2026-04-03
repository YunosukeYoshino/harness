#!/usr/bin/env bash
set -euo pipefail

if command -v pnpm >/dev/null 2>&1 && pnpm exec biome --version >/dev/null 2>&1; then
  pnpm exec biome check .
else
  echo "biome not installed; skipping JS lint"
fi
