# Claude Code entrypoint

最終更新: 2026-03-26
last-validated: 2026-03-30

この repo では `AGENTS.md` を主 knowledge file として扱います。  
まず `AGENTS.md` を読み、その後必要なら以下に進んでください。

- `docs/repo-map.md`
- `docs/repository-structure.md`
- `docs/architecture/system-overview.md`
- `work/README.md`

常時ルールは短く保ち、詳細は `docs/` や `.claude/skills/` に逃がします。

When compacting, always preserve: the current work item slug, modified file list, test commands, and agent invocation history.

## UI 開発フィードバックループ (必須)

Web/UI を変更したら以下を毎回実行する。`pnpm check` だけでは不十分。

1. `bash scripts/dev-smoke.sh` でビルド + サーバー起動 + curl 確認
2. `pnpm test:smoke` で Playwright E2E (ブラウザ画面の実検証)
3. E2E テストは **ブラウザ操作ファースト** — API テスト (request) だけで済ませない
4. 新画面を追加したら、その画面の E2E テストも同時に追加する
5. シードデータで初期状態が空にならないことを確認する

PostToolUse hook `post-ui-e2e-gate.sh` が `apps/web/` `packages/ui/` 変更時に自動で E2E を実行する。
失敗したらブロックされる。

## Agent / Skill 利用ルール (必須)

`.claude/agents/` と `.claude/skills/` は飾りではない。以下のタイミングで **必ず** 使う。

### 開発開始時
- 実装前に仕様化したい依頼は `spec-harness-bridge` を使い、`work/specs/active/` に prompt / spec を作ってから進める
- `harness-orchestrator` agent を起動する。これが全体のワークフローを統括する
- orchestrator が `planner` agent を呼び、`work/plans/active/` と `work/sprint-contracts/active/` を生成する
- plan なしにコードを書き始めない

### 実装中
- `tdd-driver` agent でテストファースト実装する (skill: `tdd-workflow`)
- テストが通ったら `code-reviewer` agent でレビュー (`repo-guardrails` に沿って境界・artifact・docs drift も確認)
- UI 変更後は `ui-browser-evaluator` agent で画面検証 (skill: `ui-evaluation`)

### 実装完了時
- `security-reviewer` agent でセキュリティチェック (skill: `security-review`)
- `progress-keeper` agent で `work/progress/current/` を更新 (`repo-guardrails` に従って artifact を整える)
- `docs-maintainer` agent で docs の整合性を確認 (`repo-guardrails` に従って docs/work の置き場を守る)

### セッション終了時
- `work/qa-reports/active/` に QA レポートが存在すること
- `work/handoffs/active/` にハンドオフが存在すること

### 禁止事項
- repo 内 agent の代わりに汎用サブエージェント (typescript-builder, Explore 等) だけで済ませること
- `.claude/skills/` の skill を一度も呼ばずにセッションを終了すること
- `work/` artifacts を生成せずに「完了」と報告すること
