#!/usr/bin/env bash
set -euo pipefail

# Keep post-edit work light.
pnpm quick-check >/tmp/agent-harness-post-check.log 2>&1 || {
  cat /tmp/agent-harness-post-check.log >&2
  exit 1
}

# Log to session directory if available
SESSION_PATH_FILE="/tmp/agent-harness-session-path"
if [[ -f "$SESSION_PATH_FILE" ]]; then
  session_dir="$(cat "$SESSION_PATH_FILE")"
  if [[ -d "$session_dir" ]]; then
    echo "{\"hook\":\"post-code-quality\",\"result\":\"pass\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "${session_dir}/hooks-fired.jsonl"
  fi
fi
