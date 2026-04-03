---
name: fix-pr
description: Fix GitHub or local review findings, re-verify, and loop up to 3 times before escalating.
user_invocable: true
---

## Workflow

1. **Gather findings**
   - Read review artifacts from `work/reviews/`
   - If a PR number is available, resolve the repository via `gh repo view --json owner,name -q '.owner.login + "/" + .name'`
   - Fetch PR comments via `gh api "repos/${OWNER_REPO}/pulls/${PR_NUMBER}/comments"`
   - Collect all findings and classify by priority (Critical / High / Medium / Optional)

2. **Fix Critical/High findings** (iterate each finding)
   a. Read the finding: file path, line range, description, and suggested fix
   b. Apply the fix
   c. Run the relevant test suite for the changed file to verify the fix does not break existing behavior

3. **Verify no regressions**
   - Run `pnpm check` (lint + typecheck + test) to confirm the full codebase is healthy

4. **Re-review**
   - Invoke the `/review` skill (or `code-reviewer` agent) to re-evaluate the codebase
   - Parse the new review output for any remaining Critical/High findings

5. **Retry loop** (max 3 iterations)
   - If new Critical/High findings exist, return to step 2 with the updated findings
   - Track the iteration count; do not exceed 3 total cycles

6. **Escalate or commit**
   - If Critical/High findings remain after 3 iterations:
     - Write a summary of unresolved issues to `work/reviews/escalation-{timestamp}.md`
     - Report the summary to the human and stop; do not commit
   - If all Critical/High findings are resolved:
     - Stage the changed files
     - Commit with a conventional commit message (e.g., `fix: resolve review findings`)
     - Push to the remote branch

## Rules

- Never skip a Critical or High finding
- Medium and Optional findings may be deferred; note them in the commit body if skipped
- Each iteration must produce a green `pnpm check` before re-review
- Do not modify test expectations solely to make tests pass; fix the source code
- If a finding is ambiguous, ask the human before applying a fix
