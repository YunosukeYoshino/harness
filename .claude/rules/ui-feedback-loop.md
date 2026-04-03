# UI Feedback Loop (強制)

## ルール

UI/Web ファイル (`apps/web/`, `packages/ui/`) を変更したら、**次のファイルを書く前に** 以下を実行すること:

1. `bash scripts/dev-smoke.sh` — ビルド + サーバー起動 + curl 確認
2. `pnpm test:smoke` — Playwright E2E

これは PostToolUse hook `post-ui-e2e-gate.sh` でも機械的に強制されるが、
hook が何らかの理由で発火しなかった場合に備え、手動でも実行すること。

## 禁止

- UI ファイルを 3 つ以上連続で書いてからまとめて smoke を回すこと
- `pnpm check` だけで E2E を省略すること（`pnpm check` は E2E を含むが、変更途中の中間検証が目的）
- `ui-browser-evaluator` agent を使わずに UI 実装を完了すること

## 理由

まとめて最後にチェックすると:
- どの変更で壊れたか特定が困難になる
- hook の発火実績がセッション証跡に残らず Forensics チェックが FAIL する
- 壊れた中間状態のまま次の変更を重ねるリスクがある
