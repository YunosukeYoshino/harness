#!/usr/bin/env bash
set -euo pipefail

# PreToolUse hook: When writing to apps/ or packages/src,
# warn if no active work plan exists in work/plans/active/.
# This catches "coding without a plan" early.

json="$(cat)"
tmp="$(mktemp)"
printf '%s' "$json" > "$tmp"

tool_name=$(python3 -c "
import json, sys, pathlib
p = json.loads(pathlib.Path(sys.argv[1]).read_text())
print(p.get('tool_name', ''))
" "$tmp" 2>/dev/null || echo "")

file_path=$(python3 -c "
import json, sys, pathlib
p = json.loads(pathlib.Path(sys.argv[1]).read_text())
inputs = p.get('tool_input', {}) or {}
print(inputs.get('file_path', inputs.get('path', '')))
" "$tmp" 2>/dev/null || echo "")

rm -f "$tmp"

# Only check for Edit/Write to source code
if [[ "$tool_name" != "Edit" && "$tool_name" != "Write" ]]; then
  exit 0
fi

# Only check for app/package source files (not tests, not config)
# Note: React Router v7 framework mode uses apps/web/app/ not apps/web/src/
case "$file_path" in
  */apps/*/src/*|*/apps/*/app/*|*/packages/*/src/*)
    ;;
  *)
    exit 0
    ;;
esac

# Check if any active plan exists
plan_count=$(find work/plans/active -type f -not -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')

if [[ "$plan_count" -eq 0 ]]; then
  echo "BLOCKED: No active work plan found in work/plans/active/." >&2
  echo "Create a plan first: use /harness-orchestrator or pnpm new:work-item <slug>" >&2
  # Log to session directory if available
  SESSION_PATH_FILE="/tmp/agent-harness-session-path"
  if [[ -f "$SESSION_PATH_FILE" ]]; then
    session_dir="$(cat "$SESSION_PATH_FILE")"
    if [[ -d "$session_dir" ]]; then
      echo "{\"hook\":\"pre-require-work-item\",\"file\":\"$file_path\",\"result\":\"blocked\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "${session_dir}/hooks-fired.jsonl"
    fi
  fi
  exit 2
fi
