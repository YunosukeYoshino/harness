---
title: Troubleshooting Guide
last-reviewed: 2026-03-29
---


# Troubleshooting Guide

This document covers common hook and quality gate failures, their root causes,
and the recommended recovery steps.


## `pre-protect-config.sh` blocks your edit

**Symptom**: Edit or Write to a file is rejected with
`Blocked protected config edit: <file>`.

**Cause**: The target file is listed in `config/protected-files.json`.
The PreToolUse hook prevents accidental changes to critical configuration.

**Fix**:

1. If the edit is intentional maintenance, re-run with the override:
   ```bash
   ALLOW_CONFIG_EDITS=1
   ```
2. If the edit was accidental, choose a different file or refactor so the
   protected file does not need modification.

**Reference**: `.claude/hooks/pre-protect-config.sh`


## `pre-require-work-item.sh` blocks code edit

**Symptom**: Edit or Write to `apps/*/src/*` or `packages/*/src/*` is rejected
with `BLOCKED: No active work plan found in work/plans/active/`.

**Cause**: No plan file (other than `.gitkeep`) exists in `work/plans/active/`.
The harness enforces plan-before-code.

**Fix**:

1. Create a work item:
   ```bash
   pnpm new:work-item <slug>
   ```
2. Or use the `harness-orchestrator` agent, which creates plan and sprint
   contract artifacts automatically.
3. Confirm a file now exists in `work/plans/active/` before retrying the edit.

**Reference**: `.claude/hooks/pre-require-work-item.sh`


## `post-code-quality.sh` fails after edit

**Symptom**: After an Edit or Write, the PostToolUse hook reports a failure
from `pnpm quick-check`.

**Cause**: The quick-check pipeline (`scripts/quick-check.sh`) runs lint,
typecheck, agent verification, root hygiene, doc freshness, architecture,
and skipped-test checks. Any single failure causes the hook to exit non-zero.

**Fix**:

1. Read the log for the specific error:
   ```bash
   cat /tmp/agent-harness-post-check.log
   ```
2. Run each sub-check individually to isolate the failure:
   ```bash
   pnpm lint
   pnpm typecheck
   python3 scripts/verify_agents.py
   python3 scripts/verify_root_hygiene.py
   python3 scripts/check_doc_freshness.py
   python3 scripts/check_architecture.py
   python3 scripts/verify_no_skipped_tests.py
   ```
3. Fix the reported error and re-edit the file.

**Reference**: `.claude/hooks/post-code-quality.sh`, `scripts/quick-check.sh`


## `post-ui-e2e-gate.sh` fails

**Symptom**: After editing a `.ts`, `.tsx`, or `.css` file under `apps/web/`
or `packages/ui/`, the hook reports `BLOCKED: runtime smoke failed` or
`BLOCKED: Playwright E2E failed`.

**Cause**: The hook runs the full build-and-verify pipeline:
1. `bash scripts/dev-smoke.sh` (build + server start + curl health check)
2. `pnpm test:smoke` (Playwright E2E)

Either the build failed, the dev server did not start, or an E2E assertion
failed.

**Fix**:

1. Read the detailed log:
   ```bash
   cat /tmp/agent-harness-e2e-gate.log
   ```
2. Run the smoke script manually to see live output:
   ```bash
   bash scripts/dev-smoke.sh
   ```
3. If the server starts but tests fail, run Playwright directly:
   ```bash
   pnpm test:smoke
   ```
4. Common sub-causes:
   - **Build error**: Check TypeScript or Vite errors in the log.
   - **Port conflict**: Another process holds port 3000 or 8787.
     ```bash
     lsof -i :3000
     lsof -i :8787
     ```
     Kill the orphan process and retry.
   - **Missing dependency**: Run `pnpm install` to ensure all packages are
     present.

**Reference**: `.claude/hooks/post-ui-e2e-gate.sh`, `scripts/dev-smoke.sh`


## `stop-verify.sh` blocks session end

**Symptom**: The Stop hook prevents session completion with one of:
- `BLOCKED: No work artifacts found`
- `WARNING: UI files were changed but no browser screenshots found`

**Cause**: The hook validates three conditions:
1. Harness state is valid (`verify_harness_state.py`)
2. No `.skip` or `.only` in test files (`verify_no_skipped_tests.py`)
3. At least one work artifact exists in `work/plans/active/`,
   `work/progress/current/`, or `work/qa-reports/active/`
4. If UI files were changed, screenshots must exist in
   `work/qa-reports/screenshots/`

**Fix**:

1. **Missing work artifacts**: Create the required artifacts. The quickest
   path is `pnpm new:work-item <slug>`, then fill in progress and QA
   report files.
2. **Skipped tests**: Search for `.skip` and `.only` in test files and
   remove them:
   ```bash
   python3 scripts/verify_no_skipped_tests.py
   ```
3. **Missing screenshots**: Run the `ui-browser-evaluator` agent or the
   `/ui-evaluation` skill to capture browser evidence into
   `work/qa-reports/screenshots/`.

**Reference**: `.claude/hooks/stop-verify.sh`


## `pnpm check` fails in CI

**Symptom**: The full quality gate (`scripts/check.sh`) fails. The output may
be long and cover multiple stages.

**Cause**: `pnpm check` runs five stages sequentially:
1. `pnpm quick-check` (lint, typecheck, agents, hygiene, docs, architecture,
   skipped tests)
2. `bash scripts/review-security.sh`
3. `python3 scripts/verify_harness_state.py`
4. `bash scripts/dev-smoke.sh`
5. `pnpm test:smoke`

**Fix**:

Run each stage individually to isolate which one fails:

```bash
pnpm quick-check
pnpm check:security
pnpm check:harness
pnpm check:runtime
pnpm test:smoke
```

Then follow the relevant section above for the failing stage.

**Reference**: `scripts/check.sh`


## Playwright tests hang

**Symptom**: `pnpm test:smoke` starts but never completes.

**Cause**: Playwright waits for the web server (`http://127.0.0.1:3000`) and
API server (`http://127.0.0.1:8787/health`) to become available. If either
server fails to start, the test runner hangs until the 120-second timeout.

**Fix**:

1. Check for port conflicts:
   ```bash
   lsof -i :3000
   lsof -i :8787
   ```
2. Kill orphan processes occupying those ports.
3. Verify the build succeeds independently:
   ```bash
   pnpm build:web
   pnpm build:api
   ```
4. Start each server manually and confirm it responds:
   ```bash
   pnpm start:web &
   curl -s http://127.0.0.1:3000
   pnpm start:api &
   curl -s http://127.0.0.1:8787/health
   ```
5. If the build itself fails, fix the underlying TypeScript or bundler error
   before re-running E2E tests.

**Reference**: `playwright.config.ts`
