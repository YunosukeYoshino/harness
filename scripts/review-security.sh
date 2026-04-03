#!/usr/bin/env bash
set -euo pipefail

# obvious dangerous primitives in executable source files
if rg --line-number \
  --glob '*.js' \
  --glob '*.jsx' \
  --glob '*.ts' \
  --glob '*.tsx' \
  --glob '*.mjs' \
  --glob '*.cjs' \
  --glob '*.mts' \
  --glob '*.cts' \
  --glob '*.sh' \
  --glob '*.bash' \
  --glob '*.zsh' \
  -e 'eval\(' \
  -e 'new Function\(' \
  .; then
  echo "security check failed: dangerous dynamic execution found" >&2
  exit 1
fi

# committed env files or sqlite db
if find . -maxdepth 3 \( -name ".env" -o -name ".env.*" -o -name "dev.db" -o -name "*.pem" -o -name "*.key" \) | grep -q .; then
  echo "security check failed: tracked secret-like file detected" >&2
  exit 1
fi

echo "security check passed"
