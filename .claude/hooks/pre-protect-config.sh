#!/usr/bin/env bash
set -euo pipefail

json="$(cat)"
tmp="$(mktemp)"
printf '%s' "$json" > "$tmp"

if [[ "${ALLOW_CONFIG_EDITS:-0}" == "1" ]]; then
  exit 0
fi

# Log attempt to session directory if available
_log_to_session() {
  local result="$1" file="$2"
  local session_path_file="/tmp/agent-harness-session-path"
  if [[ -f "$session_path_file" ]]; then
    local session_dir
    session_dir="$(cat "$session_path_file")"
    if [[ -d "$session_dir" ]]; then
      echo "{\"hook\":\"pre-protect-config\",\"file\":\"$file\",\"result\":\"$result\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "${session_dir}/hooks-fired.jsonl"
    fi
  fi
}

python3 - "$tmp" <<'PY'
from __future__ import annotations

import json
import pathlib
import re
import sys

payload = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
root = pathlib.Path(__file__).resolve().parents[2] if "__file__" in globals() else pathlib.Path.cwd()
config = json.loads((pathlib.Path.cwd() / "config/protected-files.json").read_text(encoding="utf-8"))
protected = set(config["protected"])

tool = payload.get("tool_name", "")
inputs = payload.get("tool_input", {}) or {}

candidates: set[str] = set()

if tool in {"Edit", "Write"}:
    path = inputs.get("file_path") or inputs.get("path")
    if path:
        candidates.add(path)
elif tool == "Bash":
    command = inputs.get("command", "")
    for item in protected:
        if item in command:
            candidates.add(item)

for candidate in list(candidates):
    normalized = candidate.lstrip("./")
    if normalized in protected:
        print(
            f"Blocked protected config edit: {normalized}. "
            "Set ALLOW_CONFIG_EDITS=1 for deliberate maintenance."
        )
        sys.exit(2)
PY

exit_code=$?
if [[ $exit_code -eq 2 ]]; then
  _log_to_session "blocked" "$file_path"
  exit 2
fi
