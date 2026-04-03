# Agent Harness Repository Guide

最終更新: 2026-03-30
last-validated: 2026-03-30

## 目的

この repo は **実アプリ + ハーネス成果物 + Codex PR review** を一体で運用するための公開テンプレートです。

## まず読む場所

- `README.md`: セットアップと主要コマンド
- `docs/repo-map.md`: repo 全体の索引
- `docs/repository-structure.md`: 配置ルール
- `docs/architecture/system-overview.md`: 依存方向
- `work/README.md`: mutable artifact の扱い

## 重要な原則

1. root は薄く保つ
2. 静的知識は `docs/`、mutable artifact は `work/` に分離する
3. runtime smoke と E2E smoke が通らない変更は Done にしない
4. 人間 review は前提にしない。PR の Codex review を必須ゲートにする
5. `test.skip` / `it.skip` / `describe.skip` を残したまま完了しない

## Repository contract

- `apps/web`: React Router v7 **framework mode**
- `apps/api`: Hono API shell
- UI 実装は Tailwind 前提
- shadcn/ui や AI Elements は **必要になった時に生成** する
- root 直下に作業文書を増やさない。静的知識は `docs/`、作業中の記録は `work/` に置く
- `apps/web` に別 router を持ち込まない
- `apps/api` に UI 依存を入れない
- `packages/app -> packages/ui` の依存は禁止

## Work artifacts

新しい作業は `pnpm new:work-item <slug>` を入口にする。

生成・運用対象:

- `work/specs/active/<slug>.prompt.md`
- `work/specs/active/<slug>.md`
- `work/plans/active/<slug>.md`
- `work/sprint-contracts/active/<slug>.md`
- `work/reviews/active/<slug>.md`
- `work/qa-reports/active/<slug>.md`
- `work/progress/current/<slug>.md`
- `work/handoffs/active/<slug>.md`
- `work/.locks/`: 並列作業時の artifact lock

`spec-first` の依頼では `spec-harness-bridge` を使って prompt / spec / plan / sprint contract を先に揃える。
コード着手前に plan と sprint contract を揃え、完了時は progress / review / QA / handoff まで更新する。

## Agent workflow

非 trivial な作業では `.claude/agents/` の project-local agent を優先して使う。

- 開始時: `harness-orchestrator`, `planner`
- 実装時: `tdd-driver`, `code-reviewer`
- UI 変更時: `ui-browser-evaluator`
- 完了時: `security-reviewer`, `progress-keeper`, `docs-maintainer`

repo 内の agent や skill を使わずに、汎用 agent だけで完了扱いにしない。

## Validation

最小でも変更内容に応じた検証を回す。基準コマンドは次のとおり。

- `pnpm quick-check`: lint / typecheck / agents / root hygiene / docs freshness / architecture / no-skips / script tests
- `pnpm check`: `quick-check` + security + harness state + runtime smoke + Playwright smoke
- `bash scripts/dev-smoke.sh`: build + server 起動 + curl による runtime smoke
- `pnpm test:smoke`: Playwright smoke

UI を触ったら `bash scripts/dev-smoke.sh` と `pnpm test:smoke` を両方通す。E2E は API request ベースだけで済ませず、ブラウザ操作を含める。

## Completion

以下が揃うまで Done ではありません。

- plan
- sprint contract
- progress 更新
- runtime smoke pass
- E2E smoke pass
- skipped test 検知 pass
- review artifact 更新
- PR の Codex review 実施
- QA report
- handoff

## Review priorities

Codex review では次を優先する。

- P0/P1 の runtime failure
- security regression
- architecture boundary violation
- `test.skip` の残置
- healthcheck や smoke test をすり抜ける変更
- docs と work artifact の不整合

## 主要コマンド

```bash
pnpm dev:web
pnpm dev:api
pnpm quick-check
pnpm check
pnpm test:smoke
pnpm new:work-item <slug>
bash tools/install-upstream-skills.sh
```

## Other Rules
1. Read repo-root global rules in `@.claude/rules/` only
2. If working inside a subroot, also read that subroot's `@.claude/rules/`
