---
title: "ADR-0001: Layered architecture with enforced boundaries"
last-reviewed: 2026-03-26
status: accepted
---

# ADR-0001: Layered architecture with enforced boundaries

## Context

Monorepo needs clear dependency direction to prevent coupling between layers.

## Decision

Adopt 8-layer architecture: schema, shared, domain, app, data, integrations, ui, and app shells (web/api). Enforce boundaries via `scripts/check_architecture.py` reading `config/architecture-boundaries.json`.

## Consequences

- Import violations are caught at lint time, not runtime.
- Adding a new package requires updating `architecture-boundaries.json`.
- `apps/web` is treated as UI layer; `apps/api` as app layer.
