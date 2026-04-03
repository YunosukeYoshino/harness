---
title: Codex PR Review and Auto-Fix Loop
last-reviewed: 2026-03-29
---


# Codex PR Review and Auto-Fix Loop

This document describes the current Codex-based PR review workflow and the
recommended enhanced flow that includes automated fix iterations.


## Current flow

1. Developer creates a PR (via `/pr` skill or manually).
2. The `codex-pr-review.yml` GitHub Actions workflow triggers on
   `pull_request` events (opened, synchronize, reopened).
3. Codex runs against the PR diff using the prompt in
   `.github/codex/prompts/review.md`.
4. Codex posts its findings as a PR comment via `actions/github-script`.
5. The developer reads the comment and manually fixes the issues.


## Recommended enhanced flow

The recommended flow adds an iterative fix-and-re-review loop using the
`/fix-pr` skill:

### Step 1: Create the PR

Use the `/pr` skill to ensure all quality gates pass before PR creation.

### Step 2: Codex review runs automatically

The `.github/workflows/codex-pr-review.yml` workflow fires on PR creation.
Codex analyzes the diff and posts findings as a PR comment.

### Step 3: Run `/fix-pr` to address findings

The `/fix-pr` skill automates the fix cycle:

1. **Gather findings**: Fetch Codex review comments via the GitHub API:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
   ```
   Also read any findings stored in `work/reviews/active/`.

2. **Categorize**: Classify each finding by severity:
   - Critical -- must fix immediately
   - High -- must fix before merge
   - Medium -- should fix if practical
   - Low/Optional -- defer if time-constrained

3. **Auto-fix Critical/High**: For each Critical or High finding:
   - Read the file path, line range, and suggested fix
   - Apply the fix
   - Run the relevant test suite to verify no regressions

4. **Verify**: Run `pnpm check` to confirm the full codebase is healthy.

5. **Push fixes**: Stage, commit (conventional commit: `fix: resolve review findings`),
   and push to the PR branch.

6. **Re-request review**: The push triggers `codex-pr-review.yml` again
   via the `synchronize` event.

### Step 4: Repeat (max 3 iterations)

The `/fix-pr` skill tracks iteration count. It repeats Steps 3-6 up to
3 times total. Each iteration targets only the remaining Critical/High
findings from the latest Codex review.

### Step 5: Escalate unresolved findings

If Critical or High findings remain after 3 iterations:

- The skill writes a summary to `work/reviews/escalation-{timestamp}.md`
- It reports the unresolved issues to the human developer
- It does **not** commit or push in this state
- Human judgment is required to resolve the remaining findings


## Future automation

The current flow requires the developer to manually invoke `/fix-pr` after
each Codex review. A fully automated loop could be achieved by:

1. Adding a GitHub Actions step after the Codex review job that triggers
   Claude Code via a webhook or repository dispatch event.
2. Claude Code receives the review findings, runs the fix loop, and pushes
   the result.
3. The push triggers another Codex review automatically.

This would create a fully autonomous review-fix cycle, with human escalation
only for findings that cannot be resolved within the retry budget.


## Commands reference

### Fetch PR comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

### Fetch PR review comments (inline review threads)

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews
```

### Fetch issue comments (general PR discussion)

```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments
```

### Related skills and agents

| Skill/Agent | Purpose |
|-------------|---------|
| `/pr` | Create PR with quality gate verification |
| `/fix-pr` | Iterative fix loop (max 3 retries) |
| `/review` | 3-agent parallel review (code quality, performance, spec) |
| `repo-guardrails` skill | Shared review guardrails for boundaries, artifacts, and docs drift |
| `code-reviewer` agent | Code quality and security review |
