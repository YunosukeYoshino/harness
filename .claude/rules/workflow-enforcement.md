# Workflow Enforcement (強制)

## 開発開始時 (MUST)

1. `/harness-orchestrator` skill を最初に起動する
2. `work/plans/active/` に plan を作成する (hook がブロックする)
3. `work/sprint-contracts/active/` に sprint contract を作成する
4. plan なしにソースコードを書き始めない

`pre-require-work-item.sh` が plan なしのソースコード編集を **ブロック** する (exit 2)。
回避せず、先に plan を作ること。

## 実装中 (MUST)

- `tdd-driver` agent でテストファースト
- `code-reviewer` agent でレビュー
- UI 変更後は `ui-browser-evaluator` agent で検証 (ui-feedback-loop.md 参照)

## UI 変更時の追加要件 (MUST)

`apps/web/` または `packages/ui/` を変更した場合、以下が **全て** 必要:

1. `ui-browser-evaluator` agent を起動する
2. 全ルートの agent-browser スクリーンショットが `work/qa-reports/screenshots/` に存在する
3. コンソールエラー (ブラウザ拡張由来を除く) がゼロである
4. ブラウザ QA レポートが `work/qa-reports/active/` に存在する

`stop-verify.sh` が UI 変更時にスクリーンショット証跡の有無をチェックする。
「CI が通った」だけでは完了にできない。

## 完了時 (MUST)

以下が揃わないと `stop-verify.sh` が **ブロック** する:
- `work/plans/active/` に plan
- `work/progress/current/` に progress
- `work/qa-reports/active/` に QA report
- UI 変更がある場合: `work/qa-reports/screenshots/` にスクリーンショット証跡

`work/handoffs/active/` にハンドオフも作成すること。
