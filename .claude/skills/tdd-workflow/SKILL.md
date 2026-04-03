---
name: tdd-workflow
description: Enforce small red-green-refactor loops and prevent skipped tests.
disable-model-invocation: true
---

Rules:

- Start from a failing test
- Make the minimum change to pass
- Refactor only after green
- Do not leave `test.skip`, `it.skip`, or `describe.skip`
