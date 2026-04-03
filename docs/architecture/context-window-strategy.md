---
title: Context Window Management Strategy
last-reviewed: 2026-03-29
---

# Context Window Management Strategy

AIエージェントが長時間セッションで効率的に動作するためのコンテキストウィンドウ管理戦略。

## Initializer Pattern

`harness-orchestrator` は全てのサブエージェントを直接実行するのではなく、
初期コンテキストを構築してから専門エージェントに委譲する。

```
orchestrator
  1. Read plan + sprint contract
  2. Identify affected files/packages
  3. Build focused context summary
  4. Delegate to specialized agent WITH summary (not full files)
```

各サブエージェントは、タスクに必要な最小限のコンテキストのみを受け取る。

## Context Budget Per Agent

| Agent | Expected Context | Strategy |
|-------|-----------------|----------|
| planner | Plan + codebase structure | Read repo-map.md, not full source |
| tdd-driver | Test file + implementation file + plan steps | 2-3 files max per cycle |
| code-reviewer | Changed files + architecture boundaries | git diff + boundaries.json |
| security-reviewer | Changed files + security policy | git diff + security-engineering.md |
| ui-browser-evaluator | Routes + screenshots | Route list + browser output only |
| docs-maintainer | Changed docs + repo-map | Focused diff, not full docs/ |

## Checkpoint Strategy

30分を超えるタスクでは、中間状態を永続化してコンテキストをリフレッシュする。

1. `work/progress/current/{slug}.md` に done/next/blockers を書き出す
2. サブエージェントを新規起動し、progress ファイルから再開する
3. 前のサブエージェントの出力全体を引き継がない

## Large Task Decomposition

コンテキスト予算を超えそうなタスクは、実装前に分割する。

1. `task-issue-creator` agent でDDDレイヤー別にissueを分割
2. 各issueを独立したサブエージェントセッションで実装
3. 1セッション = 1issue = 1ブランチ を原則とする

## Anti-Patterns

避けるべきパターン:

- **Full file dump**: ファイル全体をコンテキストに載せる代わりに、該当箇所のみ抽出する
- **Output accumulation**: orchestrator が全サブエージェントの出力を蓄積する。代わりに各エージェントが `work/` に結果を書き出し、orchestrator はサマリのみ読む
- **Redundant reads**: 同じファイルを複数エージェントが繰り返し読む。共通コンテキストは plan に集約する
- **Unbounded history**: 過去のセッションの全履歴を読み込む。代わりに `work/handoffs/active/` の最新ハンドオフのみ参照する
