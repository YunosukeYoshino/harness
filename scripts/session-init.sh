#!/usr/bin/env bash
set -euo pipefail

# Initialize a session directory under work/sessions/.
# Idempotent: if a session already exists (path file present and dir exists), reuse it.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SESSION_PATH_FILE="/tmp/agent-harness-session-path"

# Reuse existing session if it is still valid
if [[ -f "$SESSION_PATH_FILE" ]]; then
  existing="$(cat "$SESSION_PATH_FILE")"
  if [[ -d "$existing" && -f "$existing/session-manifest.json" ]]; then
    echo "$existing"
    exit 0
  fi
fi

# Create a new session directory
timestamp="$(date '+%Y-%m-%d_%H%M%S')"
session_dir="${REPO_ROOT}/work/sessions/${timestamp}"
mkdir -p "$session_dir"

# Write initial manifest
python3 -c "
import json, datetime
manifest = {
    'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'agents_invoked': [],
    'hooks_fired': [],
    'artifacts_created': []
}
print(json.dumps(manifest, indent=2))
" > "${session_dir}/session-manifest.json"

# Persist the session path for other hooks
printf '%s' "$session_dir" > "$SESSION_PATH_FILE"

echo "$session_dir"
