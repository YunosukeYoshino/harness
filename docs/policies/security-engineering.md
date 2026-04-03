---
title: Security engineering
last-reviewed: 2026-03-26
---


# Rules

- 秘密情報を commit しない
- healthcheck 以外の public endpoint に認証抜けを作らない
- PII をログしない
- `eval`, `new Function`, 無検証 shell 実行を避ける
- third-party integration 追加時は `docs/stack-profiles/` に追記する

## Runtime checks

`pnpm check:security` は deterministic な最低限の guard です。  
本格的な review は PR の Codex review で補完します。

