# Hook pattern must match actual framework directory conventions

**Date**: 2026-04-03
**Incident**: `pre-require-work-item.sh` used `*/apps/*/src/*` pattern, but React Router v7 framework mode places source in `apps/web/app/`. Web app source edits bypassed plan-enforcement entirely.
**Root cause**: Hook pattern was written for the `src/` convention without accounting for React Router v7's `app/` directory convention.
**Rule**: When adding or modifying hook path patterns, verify against the actual directory layout of every workspace. Run `find apps packages -maxdepth 2 -type d` to confirm.
**Enforcement**: Manual review during hook changes. `harness-auditor` skill checks patterns against actual directories.
**Verification**: `bash -c 'case "apps/web/app/root.tsx" in */apps/*/app/*) echo MATCH;; *) echo MISS;; esac'` must output MATCH.
