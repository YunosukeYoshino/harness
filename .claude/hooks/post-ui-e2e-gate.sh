#!/usr/bin/env bash
set -euo pipefail

# PostToolUse hook: Web/UI file changes trigger E2E verification.
# Only fires when apps/web/ or packages/ui/ files are edited.
# Runs the full build + runtime smoke + Playwright E2E suite.

json="$(cat)"
tmp="$(mktemp)"
printf '%s' "$json" > "$tmp"

file_path=$(python3 -c "
import json, sys, pathlib
p = json.loads(pathlib.Path(sys.argv[1]).read_text())
inputs = p.get('tool_input', {}) or {}
print(inputs.get('file_path', inputs.get('path', '')))
" "$tmp" 2>/dev/null || echo "")

rm -f "$tmp"

# Only trigger for web/ui file changes
if [[ -z "$file_path" ]]; then
  exit 0
fi

case "$file_path" in
  */apps/web/*|*/packages/ui/*)
    ;;
  *)
    exit 0
    ;;
esac

# Skip if not a source file
case "$file_path" in
  *.tsx|*.ts|*.css)
    ;;
  *)
    exit 0
    ;;
esac

log="/tmp/agent-harness-e2e-gate.log"

echo "UI change detected: $file_path" > "$log"
echo "Running E2E gate check..." >> "$log"

# Run runtime smoke (builds + starts servers + curl checks)
if ! bash scripts/dev-smoke.sh >> "$log" 2>&1; then
  echo "BLOCKED: runtime smoke failed after UI change." >&2
  echo "See $log for details." >&2
  cat "$log" >&2
  exit 1
fi

# Run Playwright E2E
if ! pnpm test:smoke >> "$log" 2>&1; then
  echo "BLOCKED: Playwright E2E failed after UI change." >&2
  echo "See $log for details." >&2
  cat "$log" >&2
  exit 1
fi

echo "E2E gate passed for: $file_path" >> "$log"

# Record UI change for stop-verify screenshot check
mkdir -p /tmp/agent-harness-ui-changes
echo "$file_path" >> /tmp/agent-harness-ui-changes/changed-files.txt

# Log to session directory if available
SESSION_PATH_FILE="/tmp/agent-harness-session-path"
if [[ -f "$SESSION_PATH_FILE" ]]; then
  session_dir="$(cat "$SESSION_PATH_FILE")"
  if [[ -d "$session_dir" ]]; then
    echo "{\"hook\":\"post-ui-e2e-gate\",\"file\":\"$file_path\",\"result\":\"pass\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "${session_dir}/hooks-fired.jsonl"
  fi
fi
