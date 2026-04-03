# apps/api guide

最終更新: 2026-03-26

## Purpose

Cloudflare Workers 上で動く Hono API と healthcheck を置く場所です。

## Rules

- `GET /health` を消さない
- 認証や認可を入れる時は fail-closed にする
- stack trace や秘密情報を response に出さない
- UI layer を import しない
- Node adapter 前提の実装を持ち込まない

## Review guidelines

- healthcheck を壊していないか
- response shape を無断で変更していないか
- 認証抜けや PII logging がないか
