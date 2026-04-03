---
title: Spec-first workflow
last-reviewed: 2026-03-30
last-validated: 2026-03-30
---

# Spec-first workflow

`spec-harness-bridge` は、すぐに実装へ入る前に仕様を固めたい時の入口です。

## いつ使うか

- 「仕様から始めたい」
- 「先に spec を作りたい」
- 「要件を固めてから実装したい」

## 何が生成されるか

- `work/specs/active/<slug>.prompt.md`
- `work/specs/active/<slug>.md`
- `work/plans/active/<slug>.md`
- `work/sprint-contracts/active/<slug>.md`

## 実装フェーズへどう渡すか

1. `spec-harness-bridge` で prompt / spec / plan / sprint contract を揃える
2. 実装に入る時点で `dev` を使う
3. 全体の進行管理が必要なら `harness-orchestrator` agent に渡す
