#!/usr/bin/env bash
set -euo pipefail

# Log an agent invocation to the current session.
# Usage: bash scripts/log-agent-invocation.sh <agent-name>

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <agent-name>" >&2
  exit 1
fi

agent_name="$1"
SESSION_PATH_FILE="/tmp/agent-harness-session-path"

# If no session exists, try to initialize one
if [[ ! -f "$SESSION_PATH_FILE" ]]; then
  REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
  bash "${REPO_ROOT}/scripts/session-init.sh" > /dev/null 2>&1 || true
fi

if [[ ! -f "$SESSION_PATH_FILE" ]]; then
  echo "WARNING: No active session. Agent invocation not logged." >&2
  exit 0
fi

session_dir="$(cat "$SESSION_PATH_FILE")"

if [[ ! -d "$session_dir" ]]; then
  echo "WARNING: Session directory does not exist: $session_dir" >&2
  exit 0
fi

# Append JSONL entry
python3 -c "
import json, datetime, sys
entry = {
    'agent': sys.argv[1],
    'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
print(json.dumps(entry))
" "$agent_name" >> "${session_dir}/agents-invoked.jsonl"
