---
title: Repository structure
last-reviewed: 2026-03-26
last-validated: 2026-03-30
---


# Structure

## Repository contract

この repo は次を維持する前提で構成します。

1. root は薄く保つ
2. 静的知識は `docs/`、mutable artifact は `work/` に分離する
3. runtime smoke と E2E smoke を completion gate にする
4. PR の Codex review を必須ゲートにする
5. Claude / Codex 向けの hooks / skills / agents は project-local に置く

## Root

root 直下には入口ファイルと config だけを置きます。  
設計説明や作業記録は root に増やしません。

## `apps/`

- `apps/web`: React Router v7 framework mode の Web shell
- `apps/api`: Hono API shell

## `packages/`

- `domain`: entity / port
- `app`: use case
- `data`: in-memory や adapter
- `integrations`: Prisma / Supabase などの外部結合
- `ui`: app から再利用する UI building blocks
- `shared`: env / util / common primitive
- `schema`: zod schema / contract

## `docs/`

静的知識を置く場所です。  
将来も読む価値があるものだけを入れます。

## `work/`

タスクごとに変化する artifact を置きます。  
root に `PLAN.md` や `QA.md` を散らさないための領域です。
spec-first の prompt / spec も `work/specs/` に置きます。

## `.claude/`

- `agents/`: 専門 subagent
- `skills/`: local reusable workflow
- `hooks/`: deterministic guardrail
- `settings.json`: project-level hook config

## `.github/`

- `ci.yml`: install + quick checks + runtime smoke + Playwright smoke
- `codex-pr-review.yml`: PR の Codex review
