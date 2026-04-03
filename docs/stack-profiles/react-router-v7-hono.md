---
title: React Router v7 + Hono
last-reviewed: 2026-03-26
---


# Stack profile

- Web: React Router v7 framework mode
- API: Hono Cloudflare Workers
- Styling: Tailwind
- Optional UI generation: shadcn/ui, AI Elements, Taste Skill

## Why

- React Router は framework mode で route module / loader / action を扱える
- Hono は Web Standards ベースで小さく、Cloudflare Workers を含む複数 runtime で動く
- smoke test の対象を `web` と `api` で分けやすい
