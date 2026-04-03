---
title: System overview
last-reviewed: 2026-03-26
---


# Overview

このテンプレートは **apps + packages + work artifacts** の 3 層で構成します。

## Apps

- `web`: UI と route module
- `api`: HTTP endpoint と healthcheck

## Packages

- `domain`: 最も安定した core model
- `app`: use case orchestration
- `data`: in-memory / adapter
- `integrations`: 外部 SDK や DB
- `ui`: 再利用 UI
- `shared`: cross-cutting helper
- `schema`: contract / validation

## Dependency rule

- `domain` は `ui` に依存しない
- `app` は `ui` に依存しない
- `web` は `app` / `domain` / `shared` / `schema` / `ui` を読める
- `api` は `app` / `domain` / `shared` / `schema` / `data` / `integrations` を読める

詳細は `docs/architecture/boundaries.md` と `config/architecture-boundaries.json`

