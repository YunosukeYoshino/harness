#!/usr/bin/env bash
set -euo pipefail

pnpm lint
pnpm typecheck
python3 scripts/verify_agents.py
python3 scripts/verify_root_hygiene.py
python3 scripts/check_doc_freshness.py
python3 scripts/check_architecture.py
pnpm check:deps
python3 scripts/verify_no_skipped_tests.py
pnpm test:scripts
