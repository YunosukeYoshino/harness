---
name: review
description: Repository review entrypoint for requests like レビューして, 監査して, 問題点を見て, 改善点を洗い出して. Runs parallel code, performance/security, and spec-consistency review, then consolidates actionable findings.
user_invocable: true
---

## Workflow

実装を進めること自体が主目的なら `dev` を使い、この skill は評価・監査・改善点抽出が主目的の時に使う。

### Step 1: Launch 3 review agents in parallel

CRITICAL: All 3 agents MUST be launched in a SINGLE message using multiple Agent tool calls. Do NOT launch them sequentially. Send one message containing all three Agent invocations at once.

Launch the following agents in parallel:

1. **code-reviewer** agent
   - Focus: code quality, test conventions, runtime regressions, boundary violations
   - Check test-conventions compliance (no `.skip`, no `.only`, naming, E2E coverage)
   - Verify docs are in sync with implementation

2. **perf-reviewer** agent
   - Focus: OWASP Top 10, N+1 queries, resource leaks, performance
   - Check for injection, XSS, auth bypass, sensitive data exposure
   - Check for unbounded queries, memory leaks, blocking I/O, bundle size

3. **spec-reviewer** agent
   - Focus: specification consistency, over-engineering detection
   - Compare implementation against plan in `work/plans/active/`
   - Flag premature abstractions, unnecessary complexity, scope creep
   - Flag missing boundary validation, insufficient error messages

### Step 2: Collect and consolidate results

After all 3 agents return:

1. Gather all findings from each agent
2. Deduplicate overlapping findings (keep the more detailed version)
3. Sort by severity: Critical > High > Medium > Low

### Step 3: Gate on Critical and High findings

If any Critical or High findings exist:
- List each finding with its agent source, file, line, and description
- State clearly: "Critical/High findings must be fixed before proceeding"
- Do NOT mark the review as passed

If no Critical or High findings exist:
- Summarize Medium and Low findings as recommendations
- Mark the review as passed

### Step 4: Write review results

Write the consolidated review report to `work/reviews/active/` with the following structure:

```
## Review Report — <date>

### Status: PASS | FAIL

### Critical / High (must fix)
- [agent] severity | file:line | description | fix suggestion

### Medium / Low (recommended)
- [agent] severity | file:line | description | fix suggestion

### Summary
- Total findings: N
- Critical: N, High: N, Medium: N, Low: N
- Agents: code-reviewer, perf-reviewer, spec-reviewer
```
