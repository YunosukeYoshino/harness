---
title: Architecture boundaries
last-reviewed: 2026-03-26
---


# Allowed imports

| owner | can import |
|---|---|
| web | ui, shared, schema, domain |
| api | app, domain, shared, schema, data, integrations |
| domain | shared, schema |
| app | domain, shared, schema |
| data | domain, shared, schema |
| integrations | domain, shared, schema |
| ui | shared, schema |
| shared | なし |
| schema | なし |

`packages/app -> packages/ui` は禁止です。  
`apps/api -> packages/ui` も禁止です。

