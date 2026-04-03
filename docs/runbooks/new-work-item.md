---
title: New work item
last-reviewed: 2026-03-26
---


# Start a work item

```bash
pnpm new:work-item todo-app
```

生成されるもの:

- `work/specs/active/todo-app.prompt.md`
- `work/specs/active/todo-app.md`
- `work/plans/active/todo-app.md`
- `work/sprint-contracts/active/todo-app.md`
- `work/reviews/active/todo-app.md`
- `work/qa-reports/active/todo-app.md`
- `work/progress/current/todo-app.md`
- `work/handoffs/active/todo-app.md`

## Completion

完了時は:

1. progress を更新
2. runtime smoke を通す
3. E2E smoke を通す
4. Codex review を実行
5. QA report と handoff を埋める
