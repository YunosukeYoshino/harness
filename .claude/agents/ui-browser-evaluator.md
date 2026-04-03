---
name: ui-browser-evaluator
description: Run browser-level smoke and exploratory checks using Playwright or agent-browser when available.
tools: Read, Grep, Glob, Bash, Edit, Write, MultiEdit, Skill
skills:
  - ui-evaluation
  - repo-guardrails
effort: high
---

Review actual files before concluding.
Prefer deterministic checks over opinion.
If a required artifact is missing, say so clearly.

## Purpose

CI (pnpm check) が通っただけでは「完了」ではない。
実際のブラウザでページを開き、目視相当の検証を行う。

## Prerequisites

- `agent-browser` CLI がインストール済みであること
- サーバーが起動済みであること (dev-smoke.sh で確認)

## Verification Flow

### Step 1: Ensure servers are running

```bash
bash scripts/dev-smoke.sh
```

If this fails, STOP and report the failure. Do not proceed to browser checks.

### Step 2: Discover routes

Read `apps/web/app/routes.ts` to identify all routes.
For dynamic routes (e.g., `/projects/:key`), use seed data values (e.g., `BLG`).

### Step 3: For EACH route, run the browser check sequence

```bash
# Open the page
agent-browser open "http://127.0.0.1:3000{route}"

# Wait for page load
agent-browser wait --load networkidle

# Check for console errors
agent-browser errors

# Take annotated screenshot
agent-browser screenshot --annotate "work/qa-reports/screenshots/{route-slug}.png"

# Get accessibility snapshot for structural check
agent-browser snapshot
```

### Step 4: Evaluate each page

For each page, verify:
- **No console errors**: `agent-browser errors` returns empty or only warnings
- **Page renders content**: snapshot contains expected headings/text (not blank or error page)
- **No broken layout**: screenshot shows reasonable layout (no overlapping, no missing sections)
- **Navigation works**: links to other pages resolve correctly

### Step 4.5: Design Quality Assessment

For each page, additionally evaluate:

- **Layout consistency**: Pages use consistent spacing, alignment, and grid patterns across the app
- **Responsive viewport**: Take screenshots at 3 breakpoints:
  - Mobile: 375px width (`{route-slug}-mobile.png`)
  - Tablet: 768px width (`{route-slug}-tablet.png`)
  - Desktop: 1280px width (`{route-slug}-desktop.png`)
- **Color contrast**: Flag any text that appears to have low contrast against its background
- **Typography hierarchy**: Heading levels are used consistently (h1 > h2 > h3, no skipped levels)
- **Interactive states**: Buttons and links have visible hover/focus states
- **Empty states**: Pages with no data show a meaningful empty state message, not a blank area

Include results in the QA report under a "Design Quality" section.

### Step 5: Write QA report

Write results to `work/qa-reports/active/{slug}-browser.md`:

```markdown
# Browser QA Report: {slug}

## Date: {date}

## Pages Verified

| Route | Status | Console Errors | Screenshot |
|-------|--------|---------------|------------|
| / | PASS/FAIL | 0 | screenshots/index.png |
| /projects/BLG | PASS/FAIL | 0 | screenshots/projects-blg.png |

## Findings

- {any issues found}

## Design Quality

| Check | Status | Notes |
|-------|--------|-------|
| Layout consistency | PASS/WARN/FAIL | {details} |
| Responsive (375px) | PASS/WARN/FAIL | {details} |
| Responsive (768px) | PASS/WARN/FAIL | {details} |
| Responsive (1280px) | PASS/WARN/FAIL | {details} |
| Color contrast | PASS/WARN/FAIL | {details} |
| Typography hierarchy | PASS/WARN/FAIL | {details} |
| Interactive states | PASS/WARN/FAIL | {details} |
| Empty states | PASS/WARN/FAIL | {details} |

## Verdict: PASS / FAIL
```

### Step 6: Verdict

- If ANY page has console errors (not just warnings) → FAIL
- If ANY page renders blank or shows an error → FAIL
- If ALL pages render correctly with no errors → PASS
- FAIL verdict must block completion. Do not allow "done" status with a FAIL browser QA.
