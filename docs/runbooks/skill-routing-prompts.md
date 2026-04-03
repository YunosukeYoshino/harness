---
title: Skill routing prompts
last-reviewed: 2026-03-30
last-validated: 2026-03-30
---

# Skill routing golden prompts

`dev` と `review` の発火確認に使う短い golden prompt 集。
skill 監査や改善ループのたびに、まずこの 2 本で routing を見る。

## `spec-harness-bridge`

期待:

- `spec-harness-bridge` が spec-first 依頼の初動候補に入る
- prompt / spec / plan / sprint contract を揃えてから実装へ渡す

プロンプト:

```text
この repo では、まず仕様から始めたいです。
課題一覧の担当者フィルタ追加について、先に spec を作って、
prompt / plan / sprint contract までそろえてください。
```

## `dev`

期待:

- `dev` が初動で候補に入る
- 実装フロー、work artifact、TDD、smoke/E2E、review/handoff を前提に進める

プロンプト:

```text
この repo で新しい機能を実装してほしいです。
課題一覧に担当者フィルタを追加して、関連テストも更新してください。
この repo の標準フローに従って、必要な work artifact と検証まで進めてください。
```

## `review`

期待:

- `review` が初動で候補に入る
- 実装そのものではなく、問題点・改善点・リスクの抽出モードに入る

プロンプト:

```text
この repo をレビューして、足りていない点と改善点を洗い出してください。
特に hooks、agents、skills の連携が弱い箇所を監査して、
優先度つきで指摘してください。
```

## 判定メモ

- `dev` prompt で `review` だけが強く出るなら、実装トリガーが弱い
- `review` prompt で `dev` に寄るなら、監査トリガーが弱い
- どちらも発火しないなら、description の先頭語彙を見直す
