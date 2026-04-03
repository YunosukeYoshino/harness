#!/usr/bin/env bash
set -euo pipefail

# Stop hook: verify harness state + no skipped tests + work artifacts + agent invocations

python3 scripts/verify_harness_state.py
python3 scripts/verify_no_skipped_tests.py

# --- Session log consolidation ---
SESSION_PATH_FILE="/tmp/agent-harness-session-path"
if [[ -f "$SESSION_PATH_FILE" ]]; then
  session_dir="$(cat "$SESSION_PATH_FILE")"
  if [[ -d "$session_dir" ]]; then
    # Copy /tmp/ logs to session directory for persistence
    for tmp_log in /tmp/agent-harness-post-check.log /tmp/agent-harness-e2e-gate.log; do
      if [[ -f "$tmp_log" ]]; then
        cp "$tmp_log" "${session_dir}/" 2>/dev/null || true
      fi
    done
    if [[ -d /tmp/agent-harness-ui-changes ]]; then
      cp -r /tmp/agent-harness-ui-changes "${session_dir}/ui-changes" 2>/dev/null || true
    fi
  fi
fi

# --- Agent invocation verification (blocking for source changes) ---
if [[ -f "$SESSION_PATH_FILE" ]]; then
  session_dir="$(cat "$SESSION_PATH_FILE")"
  agents_log="${session_dir}/agents-invoked.jsonl"
  if [[ -f "$agents_log" ]]; then
    source_changed=false
    if git diff --name-only HEAD~5 2>/dev/null | grep -qE '^apps/|^packages/'; then
      source_changed=true
    fi
    if git diff --name-only 2>/dev/null | grep -qE '^apps/|^packages/'; then
      source_changed=true
    fi

    if [[ "$source_changed" == "true" ]]; then
      if ! grep -q '"code-reviewer"' "$agents_log" 2>/dev/null && ! grep -q '"tdd-driver"' "$agents_log" 2>/dev/null; then
        echo "BLOCKED: Source code was changed but neither code-reviewer nor tdd-driver agent was invoked." >&2
        echo "Run /review skill before completing. Set SKIP_AGENT_CHECK=1 to override." >&2
        if [[ "${SKIP_AGENT_CHECK:-}" != "1" ]]; then
          exit 1
        fi
      fi
    fi
  else
    echo "WARNING: No agent invocation log found. Session tracking may not be initialized." >&2
    echo "Run: bash scripts/session-init.sh" >&2
  fi
fi

# --- Work artifact existence check ---
work_dirs=("work/plans/active" "work/progress/current" "work/qa-reports/active")
has_artifacts=false

for dir in "${work_dirs[@]}"; do
  if [[ -d "$dir" ]]; then
    count=$(find "$dir" -type f -not -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$count" -gt 0 ]]; then
      has_artifacts=true
      break
    fi
  fi
done

if [[ "$has_artifacts" == "false" ]]; then
  echo "BLOCKED: No work artifacts found in work/plans/active, work/progress/current, or work/qa-reports/active." >&2
  echo "Create plan/progress/QA artifacts before completing. See AGENTS.md completion criteria." >&2
  exit 1
fi

# --- UI screenshot evidence check ---
ui_changed=false
if git diff --name-only HEAD~5 2>/dev/null | grep -qE '^apps/web/|^packages/ui/'; then
  ui_changed=true
fi
if git diff --name-only 2>/dev/null | grep -qE '^apps/web/|^packages/ui/'; then
  ui_changed=true
fi

if [[ "$ui_changed" == "true" ]]; then
  screenshot_count=$(find work/qa-reports/screenshots -type f -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$screenshot_count" -eq 0 ]]; then
    echo "WARNING: UI files were changed but no browser screenshots found in work/qa-reports/screenshots/." >&2
    echo "Run ui-browser-evaluator agent or /ui-evaluation skill to capture browser evidence." >&2
  fi

  # Check agent invocation for UI changes
  if [[ -f "$SESSION_PATH_FILE" ]]; then
    session_dir="$(cat "$SESSION_PATH_FILE")"
    agents_log="${session_dir}/agents-invoked.jsonl"
    if [[ -f "$agents_log" ]] && ! grep -q '"ui-browser-evaluator"' "$agents_log" 2>/dev/null; then
      echo "WARNING: UI files were changed but ui-browser-evaluator agent was not invoked." >&2
    fi
  fi
fi
