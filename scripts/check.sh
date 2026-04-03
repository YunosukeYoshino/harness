#!/usr/bin/env bash
set -euo pipefail

bash scripts/quick-check.sh
bash scripts/review-security.sh
python3 scripts/verify_harness_state.py
bash scripts/dev-smoke.sh
pnpm test:smoke
