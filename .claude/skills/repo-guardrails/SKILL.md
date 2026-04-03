---
name: repo-guardrails
description: Repository-specific guardrails for architecture boundaries, work artifacts, durable docs, and review readiness. Use from project subagents.
disable-model-invocation: true
---

Use these repository guardrails when reviewing or implementing changes:

## Architecture boundaries

- `packages/app -> packages/ui` is forbidden
- `apps/api -> packages/ui` is forbidden
- `domain` stays stable and UI-free

## Artifact placement

- Durable knowledge belongs in `docs/`
- Mutable task state belongs in `work/`
- Do not add new root markdown files
- Update `docs/repo-map.md` when the repository shape changes

## Review readiness

- Check runtime regressions, boundary violations, missing tests, and docs drift
- Confirm required work artifacts exist before calling work complete
- Prefer deterministic checks over opinion
