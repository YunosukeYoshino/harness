---
title: Completed work item example
last-reviewed: 2026-04-03
---

# Example: Completed Work Item

This shows every artifact produced during a real harness-managed work item.
Use this as a reference for what a complete workflow looks like end-to-end.

## Scenario

**Task**: Add a `/health` endpoint to the API that returns server status and uptime.

**Slug**: `api-health-endpoint`

---

## 1. Scaffold

```bash
pnpm new:work-item api-health-endpoint
```

Creates:
```
work/
  plans/active/api-health-endpoint.md
  sprint-contracts/active/api-health-endpoint.md
  progress/current/api-health-endpoint.md
  qa-reports/active/api-health-endpoint.md
  handoffs/active/api-health-endpoint.md
```

## 2. Spec (`work/specs/active/api-health-endpoint-spec.md`)

```yaml
---
slug: api-health-endpoint
status: approved
created: 2026-04-01
---
```

```markdown
# API Health Endpoint

## User prompt
Add a /health endpoint that returns server status, uptime, and version.

## Acceptance criteria
- GET /health returns 200 with JSON body
- Response includes: status ("ok"), uptime (seconds), version (from package.json)
- Endpoint requires no authentication
- Response time < 50ms

## Out of scope
- Database health checks
- Dependency health checks
```

## 3. Plan (`work/plans/active/api-health-endpoint.md`)

```yaml
---
slug: api-health-endpoint
status: active
created: 2026-04-01
---
```

```markdown
# Plan: API Health Endpoint

## Approach
Add a new route in apps/api/ that returns health status.

## Steps
1. Write E2E test for GET /health (Red)
2. Add health route handler in apps/api/
3. Return status, uptime, version (Green)
4. Run code-reviewer agent
5. Update route coverage

## Files to modify
- apps/api/src/routes/health.ts (new)
- apps/api/src/index.ts (register route)
- tests/e2e/health.spec.ts (new)

## Risk
- None significant. Isolated endpoint with no dependencies.
```

## 4. Sprint contract (`work/sprint-contracts/active/api-health-endpoint.md`)

```yaml
---
slug: api-health-endpoint
status: active
created: 2026-04-01
---
```

```markdown
# Sprint Contract: api-health-endpoint

## Deliverables
- [ ] GET /health endpoint returning JSON
- [ ] E2E test covering the endpoint
- [ ] Route coverage validator updated

## Definition of done
- All tests pass
- code-reviewer agent finds no Critical/High issues
- pnpm check passes
```

## 5. Implementation (TDD cycle)

### Red: Write failing test first

```typescript
// tests/e2e/health.spec.ts
import { test, expect } from "@playwright/test";

test("GET /health returns status ok", async ({ request }) => {
  const res = await request.get("/api/health");
  expect(res.status()).toBe(200);
  const body = await res.json();
  expect(body.status).toBe("ok");
  expect(body).toHaveProperty("uptime");
  expect(body).toHaveProperty("version");
});
```

### Green: Implement the route

```typescript
// apps/api/src/routes/health.ts
import { Hono } from "hono";

const app = new Hono();
const startTime = Date.now();

app.get("/health", (c) => {
  return c.json({
    status: "ok",
    uptime: Math.floor((Date.now() - startTime) / 1000),
    version: "1.0.0",
  });
});

export default app;
```

### Hooks fired automatically
- `post-code-quality.sh` runs lint + typecheck after each file edit
- `pre-require-work-item.sh` confirms plan exists before allowing edits

## 6. Review

Agents invoked:
- `tdd-driver` -- drove the Red-Green cycle
- `code-reviewer` -- reviewed implementation (0 Critical, 0 High)
- `security-reviewer` -- confirmed no auth bypass risk (endpoint is intentionally public)

## 7. QA Report (`work/qa-reports/active/api-health-endpoint.md`)

```yaml
---
slug: api-health-endpoint
status: pass
created: 2026-04-01
---
```

```markdown
# QA Report: api-health-endpoint

## Test results
- E2E: 1/1 passed
- pnpm check: all gates passed

## Verification
- GET /health returns {"status":"ok","uptime":42,"version":"1.0.0"}
- Response time: 3ms (well under 50ms target)

## Issues found
None.
```

## 8. Progress (`work/progress/current/api-health-endpoint.md`)

```yaml
---
slug: api-health-endpoint
status: completed
created: 2026-04-01
completed: 2026-04-01
---
```

```markdown
# Progress: api-health-endpoint

## Completed
- [x] E2E test written and passing
- [x] Health route implemented
- [x] code-reviewer: 0 issues
- [x] security-reviewer: 0 issues
- [x] pnpm check: all passed

## Agents used
- tdd-driver
- code-reviewer
- security-reviewer

## Commits
- feat: add /health endpoint with uptime and version
```

## 9. Handoff (`work/handoffs/active/api-health-endpoint.md`)

```yaml
---
slug: api-health-endpoint
status: complete
created: 2026-04-01
---
```

```markdown
# Handoff: api-health-endpoint

## Summary
Added GET /health endpoint returning server status, uptime, and version.

## What was done
- New route at apps/api/src/routes/health.ts
- E2E test at tests/e2e/health.spec.ts
- All quality gates passed

## What was NOT done
- Database health checks (out of scope per spec)
- Dependency health checks (out of scope per spec)

## How to verify
1. Start the API: pnpm dev
2. curl http://localhost:8787/health
3. Run tests: pnpm test:smoke
```

## 10. Session verification

`stop-verify.sh` checks:
- [x] Plan exists in `work/plans/active/`
- [x] Progress exists in `work/progress/current/`
- [x] QA report exists in `work/qa-reports/active/`
- [x] Agent invocations logged (tdd-driver, code-reviewer)
- [x] No UI changes, so no screenshot requirement

---

## Artifact lifecycle summary

```
pnpm new:work-item api-health-endpoint
  |
  v
spec (approved) -> plan (active) -> sprint-contract (active)
  |
  v
tdd-driver: Red -> Green -> Refactor
  |
  v  (PostToolUse hooks fire on each edit)
code-reviewer + security-reviewer
  |
  v
QA report (pass) -> progress (completed) -> handoff (complete)
  |
  v
stop-verify.sh: all checks pass
```
