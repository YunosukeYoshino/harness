---
name: spec-harness-bridge
description: Spec-first workflow entrypoint for requests like 仕様から始めたい, 先にspec作って, spec-first, 要件を固めてから, 実装前に仕様化. Generates a prompt, spec, plan, and sprint contract under work/, then hands implementation to `dev`.
user_facing: true
---

# Spec-first workflow

`spec-first` の時だけ使う。すぐに実装へ入る依頼は `dev` を使う。

この skill の役割は Prompt -> Spec -> Plan に限定する。実装そのものは `dev` と repo-local agents に渡す。

## Outputs

- `work/specs/active/<slug>.prompt.md`
- `work/specs/active/<slug>.md`
- `work/plans/active/<slug>.md`
- `work/sprint-contracts/active/<slug>.md`

## Workflow

### 1. Repo constraints を読む

最低でも次を確認する。

- `AGENTS.md`
- `CLAUDE.md`
- `docs/repo-map.md`
- `docs/architecture/system-overview.md`
- `work/README.md`

`Repo Constraints` には少なくとも以下を反映する。

- `apps/web` は React Router v7 framework mode
- `apps/api` は Hono API shell
- UI 実装は Tailwind 前提
- durable docs は `docs/`、mutable artifact は `work/`
- `apps/api -> packages/ui` は禁止
- `packages/app -> packages/ui` は禁止
- runtime smoke / E2E smoke / no skipped tests / review / QA / handoff が completion gate

### 2. `<slug>` を決める

既存の work artifact 名に合わせて、短く説明的な kebab-case を使う。

### 3. prompt artifact を作る

`work/specs/active/<slug>.prompt.md` に、spec を生成するための prompt を残す。

最低限含める項目:

- original request
- repo context
- fixed spec sections
- known constraints
- open questions

### 4. spec artifact を作る

`work/specs/active/<slug>.md` に、次の見出しを固定で使う。

- `## Goal`
- `## Scope`
- `## Non-Goals`
- `## User Stories`
- `## Acceptance Criteria`
- `## Repo Constraints`
- `## Implementation Plan Summary`
- `## Risks / Open Questions`

Kiro CLI と `kiro-spec-bridge` が使えるなら下書きに使ってよい。ただし最終出力先は必ず `work/specs/active/` に統一する。

### 5. plan / sprint contract を作る

spec を基に以下を生成または更新する。

- `work/plans/active/<slug>.md`
- `work/sprint-contracts/active/<slug>.md`

plan には小さく検証可能な steps を書く。sprint contract には scope / done definition / required checks を明記する。

### 6. 実装フェーズへ handoff する

仕様が固まったら `dev` を使う。全体オーケストレーションが必要なら `harness-orchestrator` agent に渡す。

## Prompt template

```md
# Spec generation prompt

## User request

<paste the user request>

## Repo context

- Read `AGENTS.md`, `CLAUDE.md`, `docs/repo-map.md`, `docs/architecture/system-overview.md`, `work/README.md`
- Keep durable knowledge in `docs/` and mutable task state in `work/`
- Keep implementation within the existing React Router / Hono / Tailwind architecture

## Required spec sections

- Goal
- Scope
- Non-Goals
- User Stories
- Acceptance Criteria
- Repo Constraints
- Implementation Plan Summary
- Risks / Open Questions

## Output rule

Write the final spec to `work/specs/active/<slug>.md`.
```
