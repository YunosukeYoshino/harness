# Contributing

## Development setup

```bash
pnpm install
pnpm exec playwright install --with-deps chromium
pnpm check   # verify everything passes
```

## Workflow

This repository uses its own harness to enforce quality. When you work with Claude Code or Codex:

1. **Create a work item first**: `pnpm new:work-item <slug>`
2. **Plan before code**: The `pre-require-work-item.sh` hook blocks source code edits without an active plan
3. **Every edit is checked**: `post-code-quality.sh` runs lint + typecheck + validators after every file change
4. **UI changes trigger E2E**: `post-ui-e2e-gate.sh` runs build + Playwright after UI file edits
5. **Session end is gated**: `stop-verify.sh` verifies work artifacts and agent invocations exist

## Submitting changes

### Issues

- Use GitHub Issues for bug reports, feature requests, and discussions
- Include reproduction steps for bugs
- Reference the relevant harness dimension (hooks, agents, skills, artifacts, etc.)

### Pull requests

- Create a short-lived branch per feature
- Title under 70 characters
- Include a summary based on full commit history
- Include a test plan checklist
- When a related issue exists, add `Closes #<number>` in the PR body

### Commit convention

```
<type>: <description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

One commit = one logical change. Do not mix unrelated changes.

## Quality gates

All of these must pass before merge:

- `pnpm quick-check` -- lint, typecheck, architecture boundaries, doc freshness, no skipped tests
- `pnpm check` -- quick-check + security + harness state + runtime smoke + E2E
- Codex PR review (automated via GitHub Actions)

## What NOT to do

- Do not push directly to main
- Do not add `test.skip` or `.only` in committed code
- Do not place mutable artifacts in `docs/` (use `work/`)
- Do not place static knowledge in `work/` (use `docs/`)
- Do not bypass hooks with `--no-verify`

## Code style

- Biome for formatting and linting (auto-configured)
- TypeScript strict mode
- See `.claude/rules/` for additional conventions

## Questions?

Open an issue or start a discussion.
