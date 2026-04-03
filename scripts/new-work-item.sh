#!/usr/bin/env bash
set -euo pipefail

slug="${1:-}"
if [[ -z "$slug" ]]; then
  echo "Usage: pnpm new:work-item <slug>" >&2
  exit 1
fi

today="$(date +%F)"

mkdir -p work/plans/active   work/sprint-contracts/active   work/reviews/active   work/qa-reports/active   work/progress/current   work/handoffs/active
mkdir -p work/specs/active   work/specs/archive

cat > "work/specs/active/${slug}.prompt.md" <<EOF
---
title: ${slug}
status: draft
created: ${today}
---

# Spec generation prompt

## User request

- Summarize the original user request here.

## Repo context

- Read AGENTS.md, CLAUDE.md, docs/repo-map.md, docs/architecture/system-overview.md, work/README.md
- Keep durable knowledge in docs/ and mutable task state in work/
- Respect existing React Router, Hono, and Tailwind boundaries

## Required spec sections

- Goal
- Scope
- Non-Goals
- User Stories
- Acceptance Criteria
- Repo Constraints
- Implementation Plan Summary
- Risks / Open Questions
EOF

cat > "work/specs/active/${slug}.md" <<EOF
---
title: ${slug}
status: draft
created: ${today}
---

# Specification

## Goal

## Scope

## Non-Goals

## User Stories

## Acceptance Criteria

## Repo Constraints

## Implementation Plan Summary

## Risks / Open Questions
EOF

cat > "work/plans/active/${slug}.md" <<EOF
---
title: ${slug}
status: draft
created: ${today}
---

# Plan

## Goal

## Scope

## Non-goals

## Steps
EOF

cat > "work/sprint-contracts/active/${slug}.md" <<EOF
---
title: ${slug}
status: draft
created: ${today}
---

# Sprint contract

## Deliverables

## Done definition

## Required checks
EOF

cat > "work/reviews/active/${slug}.md" <<EOF
---
title: ${slug}
status: pending
created: ${today}
---

# Review log

## Codex findings

## Triage

## Fixes
EOF

cat > "work/qa-reports/active/${slug}.md" <<EOF
---
title: ${slug}
status: pending
created: ${today}
---

# QA report

## Runtime smoke

## E2E smoke

## Notes
EOF

cat > "work/progress/current/${slug}.md" <<EOF
---
title: ${slug}
status: active
created: ${today}
---

# Progress

## Done

## Next

## Blockers
EOF

cat > "work/handoffs/active/${slug}.md" <<EOF
---
title: ${slug}
status: pending
created: ${today}
---

# Handoff

## Current state

## Next command

## Risks
EOF

echo "Created work item: ${slug}"
