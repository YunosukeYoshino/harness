---
name: dev
description: Repository development entrypoint for requests like 実装して, 追加して, 修正して, この repo で作って. Handles work artifacts, TDD, smoke/E2E verification, review, and handoff.
user_facing: true
---

# Dev Workflow

Issue から handoff まで、この repo の標準開発フロー全体を統括する。
レビューや監査が主目的なら `review` を使い、この skill は実装を前に進める時に使う。

## Steps

### 1. 仕様把握

- Issue / 要件を読み、スコープを明確にする
- 曖昧な点があればユーザーに質問して解消する
- 完了条件 (acceptance criteria) を確認する

### 2. ブランチ作成

- 現在のブランチ戦略に従って作業ブランチを用意する
- 先に `work/` artifact と plan / sprint contract を揃える

ブランチ名や作成方法は、repo の現在運用を優先する。

### 3. テスト計画

- コードを書く前にテストケースを設計する
- 正常系・異常系・境界値を網羅する
- テストファイルを先に作成し、全テストが RED であることを確認する
- plan と sprint contract のステップに対応付ける

### 4. TDD 実装

- `tdd-driver` agent を使い Red-Green-Refactor サイクルで実装する
- 1 サイクルで 1 つのテストだけを GREEN にする
- `.skip` / `.only` を残さない
- 実装が完了したら `code-reviewer` agent でレビューする

### 5. 品質ゲート

`pnpm check` を実行する。失敗した場合は最大 3 回リトライする。

```
attempt = 0
while attempt < 3:
    run pnpm check
    if success: break
    attempt += 1
    fix the reported issues
if attempt == 3 and still failing:
    escalate to human with failure details
```

- 3 回リトライしても失敗する場合は、エラー内容をユーザーに報告し判断を仰ぐ
- 全パスしたらステップ 6 へ

### 6. ブラウザ検証 (UI 変更がある場合は MUST)

`apps/web/` または `packages/ui/` を変更した場合、`ui-browser-evaluator` agent を **必ず** 起動する。

```
Agent (ui-browser-evaluator):
  "Run browser verification for all routes.
   Capture screenshots to work/qa-reports/screenshots/.
   Report console errors and rendering issues."
```

agent-browser が使用可能か確認:
```bash
which agent-browser
```

以下が完了していること:
- [ ] 全ルートのスクリーンショットが `work/qa-reports/screenshots/` に存在する
- [ ] コンソールエラー (ブラウザ拡張由来を除く) がゼロである
- [ ] ブラウザ QA レポートが `work/qa-reports/active/` に存在する

UI 変更がないバックエンドのみの変更ではスキップ可。
