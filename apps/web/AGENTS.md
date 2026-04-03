# apps/web guide

最終更新: 2026-03-26

## Purpose

React Router v7 framework mode の route module と Cloudflare Workers 用の UI shell を置く場所です。

## Rules

- 別 router を導入しない
- `app/routes.ts` を route entry とする
- root shell は `app/root.tsx`
- Cloudflare 用の worker entry は `workers/app.ts`
- pending / empty / error state を省略しない
- Tailwind 前提で書く
- `wrangler dev` / `wrangler deploy` 前提の worker 実行を壊さない
- shadcn/ui は生成で入れる。手書きで似た部品を量産しない
- runtime smoke を壊す変更は accept しない

## Review guidelines

- route module export を壊していないか
- `test.skip` を残していないか
- hydration mismatch を生みそうなコードがないか
- keyboard / focus / aria を壊していないか
