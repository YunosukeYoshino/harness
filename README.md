# Agent Harness Public Template v6

[English](#what-is-this) | [日本語](#これは何か)

---

## What is this?

A **production-ready template** for [Harness Engineering](https://openai.com/index/harness-engineering/) -- the practice of building scaffolding and guardrails so AI coding agents (Claude Code, Codex, etc.) produce reliable, safe, high-quality code autonomously.

Just as a horse harness converts raw power into useful work, this template converts AI agent capabilities into trustworthy software output.

### What you get

| Layer | What | Why |
|-------|------|-----|
| **Runtime app** | React Router v7 + Hono API + 7 clean-architecture packages | Real app shell, not a toy |
| **5 hooks** | PreToolUse / PostToolUse / Stop | Mechanical enforcement -- lint, typecheck, E2E run on every edit |
| **11 agents** | orchestrator, planner, tdd-driver, 3 reviewers, security, UI, docs, progress, task-issue | Specialized delegation, not monolithic prompts |
| **9 skills** | spec-first, dev, review, PR, fix-PR, TDD, security, UI evaluation, guardrails | Reusable workflows invoked on demand |
| **7 custom validators** | architecture boundaries, root hygiene, doc freshness, route coverage, no-skip, agent defs, harness state | Beyond standard linting |
| **Work artifact system** | specs / plans / sprint-contracts / reviews / QA / progress / handoffs | Structured lifecycle tracking |
| **CI + Codex review** | GitHub Actions + automated PR review | No human review bottleneck |
| **Session forensics** | Hook firing logs, agent invocation tracking, stop-time verification | Prove compliance, not just claim it |

### Architecture

```
User request
  |
  v
/spec-harness-bridge --> specs + plan + sprint-contract
  |
  v
[PreToolUse] plan enforcement --> blocks code without plan
  |
  v
tdd-driver agent --> Red-Green-Refactor
  |
  v
[PostToolUse] auto quality gate --> lint + typecheck + dep-cruiser + 4 validators
  |                                  |
  | (UI file?)                       |
  v                                  |
[PostToolUse] E2E gate --> build + Playwright
  |
  v
code-reviewer + security-reviewer + spec-reviewer (parallel)
  |
  v
[Stop] session verification --> artifacts + agent invocations + screenshots
```

Every arrow is enforced by a hook or script, not by a suggestion in a markdown file.

---

## Quick start

```bash
git clone <this-repo> my-project
cd my-project
pnpm install
pnpm exec playwright install --with-deps chromium
pnpm check   # runs all quality gates
```

Then start building:

```bash
pnpm new:work-item my-feature   # scaffold all work artifacts
# Claude Code / Codex will follow the harness automatically
```

### Prerequisites

- Node 20+
- pnpm
- Python 3.11+ (for verification scripts)
- Playwright Chromium (installed above)

### Key commands

| Command | What it does |
|---------|-------------|
| `pnpm dev` | Start web + API in dev mode |
| `pnpm quick-check` | Fast gate: lint, typecheck, boundaries, validators (~30s) |
| `pnpm check` | Full gate: quick-check + security + harness state + smoke + E2E |
| `pnpm test:smoke` | Playwright E2E only |
| `pnpm new:work-item <slug>` | Scaffold all work artifacts for a new task |
| `bash tools/install-upstream-skills.sh` | Add React Router / Hono / shadcn skills |

---

## Customize for your project

See [docs/runbooks/customizing-template.md](docs/runbooks/customizing-template.md) for a step-by-step guide.

Short version:
1. Replace the app shell in `apps/web/` and `apps/api/` with your app
2. Adjust `config/architecture-boundaries.json` for your dependency rules
3. Update `docs/stack-profiles/` if you change the tech stack
4. Run `pnpm check` to verify everything still passes

---

## Learn more

- [AGENTS.md](AGENTS.md) -- primary knowledge file for AI agents
- [docs/repo-map.md](docs/repo-map.md) -- full repository index
- [docs/architecture/system-overview.md](docs/architecture/system-overview.md) -- architecture details
- [CONTRIBUTING.md](CONTRIBUTING.md) -- how to contribute

### Harness Engineering reading list

- [Harness engineering (OpenAI / Lopopolo)](https://openai.com/index/harness-engineering/) -- foundational article
- [Harness design for long-running apps (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps) -- Generator+Evaluator pattern
- [My AI Adoption Journey (Hashimoto)](https://mitchellh.com/writing/my-ai-adoption-journey) -- "never let the same mistake happen twice"
- [Improving Deep Agents (LangChain)](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) -- measurable harness improvement

---

## これは何か

AI コーディングエージェント (Claude Code, Codex 等) が自律的に信頼性の高いコードを出力するための「足場(ハーネス)」を構築する [Harness Engineering](https://openai.com/index/harness-engineering/) の実践テンプレートです。

### 特徴

- **5 つの hook** が毎編集で lint / typecheck / E2E を自動発火
- **11 エージェント** が専門分野ごとに分離 (TDD、レビュー、セキュリティ、UI 検証等)
- **7 つのカスタム検証** が標準リンターを超えた品質ゲートを提供
- **Work artifact システム** が spec → plan → code → review → QA → handoff のライフサイクルを管理
- **CI + Codex review** で人間レビューなしの品質保証パイプライン

### クイックスタート

```bash
git clone <this-repo> my-project && cd my-project
pnpm install
pnpm exec playwright install --with-deps chromium
pnpm check
```

詳細は [AGENTS.md](AGENTS.md) と [docs/repo-map.md](docs/repo-map.md) を参照してください。

---

## License

[MIT](LICENSE)
