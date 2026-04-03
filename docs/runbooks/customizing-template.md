---
title: Customizing the template
last-reviewed: 2026-04-03
---

# Customizing the Template

How to adapt this harness template for your own project.

## Step 1: Replace the app shell

The template ships with a minimal React Router v7 + Hono app. Replace it with your own:

```
apps/
  web/    -> your frontend (React Router v7, Next.js, etc.)
  api/    -> your backend (Hono, Express, Fastify, etc.)
```

If you change frameworks, update the stack profile:

- Edit `docs/stack-profiles/react-router-v7-hono.md` (or create a new profile)
- Update `apps/web/AGENTS.md` and `apps/api/AGENTS.md` with framework-specific guidance

## Step 2: Adjust architecture boundaries

Edit `config/architecture-boundaries.json` to match your package structure:

```json
{
  "web": ["ui", "shared", "schema", "domain"],
  "api": ["app", "domain", "shared", "schema", "data", "integrations"],
  "domain": ["shared", "schema"],
  ...
}
```

Rules:
- Each key is a workspace (directory under `apps/` or `packages/`)
- The value array lists which other workspaces it may import from
- Unlisted imports are **blocked** by dependency-cruiser

After editing, run `pnpm check:deps` to verify no violations.

## Step 3: Add or remove packages

The template includes 7 packages under `packages/`:

| Package | Purpose |
|---------|---------|
| `app` | Application services / use cases |
| `data` | Data access / repositories |
| `domain` | Domain models / business logic |
| `integrations` | External service adapters |
| `schema` | Shared schemas (Zod, etc.) |
| `shared` | Utilities shared across all layers |
| `ui` | UI components |

To add a package:
1. Create `packages/<name>/` with `package.json` (name: `@repo/<name>`)
2. Add it to `config/architecture-boundaries.json`
3. Add path mapping to `tsconfig.base.json`
4. Run `pnpm install` to link the workspace

To remove a package:
1. Delete the directory
2. Remove from `config/architecture-boundaries.json`
3. Remove path mapping from `tsconfig.base.json`
4. Remove references from other packages

## Step 4: Update hook patterns

Hooks use file path patterns to decide when to fire. If your source layout differs from the default, update:

- `.claude/hooks/pre-require-work-item.sh` -- pattern for source files (line ~34)
- `.claude/hooks/post-ui-e2e-gate.sh` -- pattern for UI files
- `.claude/hooks/post-code-quality.sh` -- pattern for lint/typecheck targets

Example: if your frontend uses `src/` instead of `app/`:
```bash
# In pre-require-work-item.sh
case "$file_path" in
  */apps/*/src/*|*/apps/*/app/*|*/packages/*/src/*)
```

Always verify patterns against your actual directory layout:
```bash
find apps packages -maxdepth 2 -type d
```

## Step 5: Configure quality gates

### Linting
The template uses Biome. To switch to ESLint:
1. Replace `biome.json` with `.eslintrc.*`
2. Update `pnpm lint` in root `package.json`
3. Update `scripts/quick-check.sh` if it references Biome directly

### Testing
- E2E: `playwright.config.ts` -- update `baseURL`, browser list, test directories
- Unit/Integration: add your test runner (Vitest, Jest) and update `pnpm test` script

### Custom validators
Scripts in `scripts/` enforce project-specific rules:
- `check_architecture.py` -- boundary validation
- `verify_no_skipped_tests.py` -- no `.skip` / `.only`
- `verify_route_coverage.py` -- E2E covers all routes
- `verify_harness_state.py` -- work artifact structure

Modify or remove validators that don't apply to your project.

## Step 6: Customize agents and skills

### Agents (`.claude/agents/`)
- Keep `harness-orchestrator`, `planner`, `code-reviewer`, `progress-keeper` as-is
- Modify `tdd-driver` if your test strategy differs
- Add domain-specific agents for your project

### Skills (`.claude/skills/`)
- `dev`, `review`, `pr`, `fix-pr` are generally reusable
- Update `spec-harness-bridge` if your spec format differs
- Add skills for your domain workflows

### Skill routing
Update `.claude/skills/repo-guardrails/SKILL.md` and `docs/runbooks/skill-routing-prompts.md` to add routing for your custom skills.

## Step 7: Verify everything

After customization, run the full pipeline:

```bash
pnpm check          # all quality gates
pnpm new:work-item test-customization  # verify work item scaffold
```

## Checklist

- [ ] App shell replaced or adapted
- [ ] `config/architecture-boundaries.json` matches your packages
- [ ] `tsconfig.base.json` path mappings updated
- [ ] Hook patterns match your directory layout
- [ ] Stack profile updated in `docs/stack-profiles/`
- [ ] Workspace AGENTS.md files updated (`apps/web/`, `apps/api/`)
- [ ] `pnpm check` passes
- [ ] `pnpm new:work-item` scaffolds correctly
