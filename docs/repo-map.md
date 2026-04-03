---
title: Repository map
last-reviewed: 2026-03-29
last-validated: 2026-03-30
---


# Index

## Entry points

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`

## Static knowledge

- `docs/architecture/*` (includes `context-window-strategy.md`)
- `docs/policies/*`
- `docs/runbooks/*` (incl. post-incident, troubleshooting, codex-review-loop, skill-routing-prompts, spec-first-workflow)
- `docs/stack-profiles/*`

## Mutable work artifacts

- `work/specs/*`
- `work/plans/*`
- `work/sprint-contracts/*`
- `work/reviews/*`
- `work/qa-reports/*`
- `work/progress/*`
- `work/handoffs/*`
- `work/.locks/*` -- artifact write locks for parallel sub-agent safety

## Runtime code

- `apps/web`
- `apps/api`
- `packages/*`

## Developer tools

- `tools/install-upstream-skills.sh` -- install upstream skills (React Router, Hono, etc.)
- `tools/README.md` -- tool documentation
- `.agents/skills/*` -- upstream skills managed by the `skills` CLI
- `.claude/skills/*` -- local skills and Claude-facing symlinks for upstream skills

## Claude / Codex integration

- `.claude/settings.json`
- `.claude/hooks/*`
- `.claude/agents/*`
- `.claude/skills/*`
- `.claude/rules/learned/*` -- rules from operational incidents (mistake-to-rule loop)
- `.github/workflows/codex-pr-review.yml`
- `.github/codex/prompts/review.md`

## Scripts

- `scripts/artifact-lock.sh` -- acquire/release/check write locks on work artifacts
- `scripts/new-work-item.sh` -- scaffold a new work item with spec, plan, and review artifacts
- `scripts/check.sh` -- full quality gate (lint, typecheck, verify, smoke, E2E)
- `scripts/quick-check.sh` -- fast quality gate (lint, typecheck, static verification)
- `scripts/verify_route_coverage.py` -- E2E route coverage enforcement
