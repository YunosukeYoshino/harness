---
name: ui-evaluation
description: Evaluate the running web app with Playwright E2E and agent-browser visual verification.
disable-model-invocation: true
---

This skill provides the full browser verification flow.
CI passing alone is NOT sufficient. Actual browser rendering must be confirmed.

## Execution Order

### Phase 1: Automated E2E (Playwright)

```bash
pnpm test:smoke
```

If E2E fails, STOP. Fix the issue before proceeding.

### Phase 2: Visual Browser Verification (agent-browser)

Requires: `agent-browser` CLI installed (`which agent-browser`).
If not installed, skip Phase 2 and note it in the report.

For each route in `apps/web/app/routes.ts`:

```bash
# 1. Open page
agent-browser open "http://127.0.0.1:3000{route}"
agent-browser wait --load networkidle

# 2. Console error check (CRITICAL)
agent-browser errors
# If errors exist → record as FAIL for this route

# 3. Screenshot with annotations
mkdir -p work/qa-reports/screenshots
agent-browser screenshot --annotate "work/qa-reports/screenshots/{route-slug}.png"

# 4. Accessibility snapshot for content verification
agent-browser snapshot
# Verify expected headings/content exist in the snapshot output
```

### Phase 2.5: Design Quality Assessment

For each route verified in Phase 2, additionally evaluate:

1. **Responsive screenshots**: Resize viewport and capture at 3 breakpoints:
   - `{route-slug}-mobile.png` (375px)
   - `{route-slug}-tablet.png` (768px)
   - `{route-slug}-desktop.png` (1280px)

2. **Design checks**:
   - Layout consistency (spacing, alignment, grid patterns)
   - Color contrast (text readability against background)
   - Typography hierarchy (h1 > h2 > h3, consistent sizing)
   - Interactive states (hover/focus visible on buttons and links)
   - Empty states (meaningful message when no data)

3. **Naming convention**: All screenshots follow `{route-slug}-{viewport}.png` format.

Include a "Design Quality" section in the QA report with PASS/WARN/FAIL per check.
WARN items do not block completion but should be noted for follow-up.

### Phase 3: Write QA Report

Write to `work/qa-reports/active/{slug}-browser.md`:

- Table of all routes with PASS/FAIL status
- Console error count per route
- Screenshot paths as evidence
- Any layout or content issues found
- Overall verdict: PASS only if ALL routes pass

### Rules

- Do NOT skip Phase 2 when agent-browser is available
- Do NOT report PASS if any page has JavaScript console errors
- Do NOT report PASS if any page renders blank content
- Screenshot evidence is REQUIRED for each verified route
- The QA report MUST exist in `work/qa-reports/active/` before completion
- The QA report MUST include a "Design Quality" section with responsive and design checks
- Screenshot naming MUST follow `{route-slug}-{viewport}.png` convention
