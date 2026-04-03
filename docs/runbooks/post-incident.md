---
title: Post-Incident Rule Creation Process
last-reviewed: 2026-03-29
---


# Post-Incident Rule Creation Process

## When to use

After any agent produces incorrect output, violates conventions, or causes a regression.
The goal is to turn every operational mistake into a permanent harness rule so it never recurs.

## Process

### 1. Identify

What exactly went wrong?

- Which file was affected?
- Which line or section?
- What was the incorrect behavior?
- What was the expected behavior?

Capture a concrete, reproducible description of the failure.

### 2. Categorize

Determine the nature of the mistake:

- **Code pattern issue**: Agent generated code that violates style, architecture, or correctness rules
- **Workflow issue**: Agent skipped a required step (e.g., tests, reviews, plan creation)
- **Context issue**: Agent lacked information that should have been available (e.g., missing docs, stale references)

### 3. Determine enforcement level

Choose the appropriate enforcement mechanism based on how strictly the rule must be applied:

| Enforcement | When to use | Location |
|---|---|---|
| Linter / verification script | Can be caught by static analysis or a script | `scripts/` |
| PreToolUse hook | Must block tool execution before it happens | `.claude/hooks/` |
| PostToolUse hook | Needs a check after execution completes | `.claude/hooks/` |
| Rule (guidance) | Is advice, not a hard block | `.claude/rules/learned/` |

### 4. Implement

Create the rule, hook, or script:

- For scripts: Add to `scripts/` and integrate into `scripts/check.sh` or `scripts/quick-check.sh`
- For hooks: Add to `.claude/hooks/` and register in `.claude/settings.json`
- For rules: Add a Markdown file to `.claude/rules/learned/`

### 5. Test

Verify the new rule catches the original mistake:

- Reproduce the original failure condition
- Confirm the rule blocks, warns, or corrects it
- Confirm the rule does not produce false positives on valid operations

### 6. Document

Add an entry to `.claude/rules/learned/` with date and incident description.
Use the filename format `YYYY-MM-DD-short-description.md`.

## Examples

### Agent deleted a file with `rm` instead of `trash`

- **Category**: Code pattern issue
- **Enforcement**: PreToolUse hook blocking `rm` commands
- **Implementation**: Hook in `.claude/hooks/` that inspects Bash commands for `rm` invocations

### Agent wrote test with `.only`

- **Category**: Code pattern issue
- **Enforcement**: Verification script
- **Implementation**: `scripts/verify_no_skipped_tests.py` (already exists)

### Agent edited protected config

- **Category**: Workflow issue
- **Enforcement**: PreToolUse hook
- **Implementation**: `scripts/pre-protect-config.sh` (already exists)
