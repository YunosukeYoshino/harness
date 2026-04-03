---
name: pr
description: Create a PR only after quality gates, work artifacts, and Codex review request preparation are complete.
user_invocable: true
---

## Workflow

### 1. Quality gates

Run `pnpm check` (lint + typecheck + test). All must pass before proceeding.
If any gate fails, fix the issue and re-run. Do not skip.

### 2. Verify work artifacts

Confirm these files exist and are non-empty:

- `work/plans/active/*.md` -- implementation plan
- `work/progress/current/*.md` -- progress log
- `work/qa-reports/active/*.md` -- QA report

If any artifact is missing, create it before continuing.

### 3. Create PR

Use `gh pr create` with the following content:

**Title**: concise, under 70 characters, conventional-commit style prefix.

**Body**:

```
## Summary
<1-3 bullet points summarizing ALL commits on this branch, not just the latest>

## Test plan
- [ ] pnpm check passes (lint, typecheck, test)
- [ ] Work artifacts present (plan, progress, QA report)
- [ ] <additional test steps relevant to the change>

Closes #<issue number if applicable>

Generated with Claude Code
```

Build the summary from `git log` and `git diff` against the base branch.
Include `Closes #N` when there is a linked issue.

### 4. Request Codex review

After the PR is created, request a review via one of:

- `codex-review-prep` skill to prepare context, then trigger Codex workflow
- Or post a PR comment: `@codex review` to invoke Codex review directly

Confirm the review request was dispatched before reporting completion.
