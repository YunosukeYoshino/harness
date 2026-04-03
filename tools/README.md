# tools/

Developer tools and scripts for the agent harness.

## Available Tools

### install-upstream-skills.sh

Install upstream skills that enhance agent capabilities for specific tech stacks.

```bash
# Install all upstream skills
bash tools/install-upstream-skills.sh

# List available skills without installing
bash tools/install-upstream-skills.sh --list

# Show usage
bash tools/install-upstream-skills.sh --help
```

**Included skills:**

| Skill | Purpose |
|-------|---------|
| react-router-framework-mode | React Router framework mode (loaders, actions, route modules) |
| hono | Hono HTTP framework |
| shadcn | shadcn/ui component generation |
| ai-elements | Vercel AI Elements |
| prisma-client-api | Prisma Client API |
| agent-browser | agent-browser visual verification |
| design-taste-frontend | Taste Skill frontend design guidance |

Installed skills are managed project-locally by `npx skills add`, with package
content under `.agents/skills/`. The installer rewrites each corresponding
`.claude/skills/<skill-name>` entry as a symlink to `.agents/skills/<skill-name>`
and validates that `.claude/skills/<skill-name>/SKILL.md` resolves correctly.

## Adding New Tools

Place new scripts in this directory. Each script should:

1. Include a shebang (`#!/usr/bin/env bash`)
2. Use `set -euo pipefail`
3. Support `--help` for usage information
4. Be idempotent (safe to run multiple times)
