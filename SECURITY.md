# Security Policy

最終更新: 2026-03-26

## Reporting

脆弱性を見つけた場合は public issue ではなく private channel で報告してください。

## Engineering rules

- 秘密情報は commit しない
- `.env*`, `*.pem`, `*.key`, `dev.db` を追跡しない
- 認証や認可の bypass を test なしで導入しない
- PII をログに出さない
- `eval`, `new Function`, 危険な shell 実行を不用意に導入しない

実装規約の詳細は `docs/policies/security-engineering.md` を見てください。
