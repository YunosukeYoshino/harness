#!/usr/bin/env bash
set -euo pipefail

# Artifact write locking for parallel sub-agent safety.
#
# Usage:
#   scripts/artifact-lock.sh acquire <artifact-path> [timeout_seconds]
#   scripts/artifact-lock.sh release <artifact-path>
#   scripts/artifact-lock.sh check <artifact-path>
#
# Lock files are stored in work/.locks/ as {artifact-basename}.lock
# Stale locks older than 5 minutes are automatically overridden.

LOCK_DIR="work/.locks"
STALE_THRESHOLD_SECONDS=300
DEFAULT_TIMEOUT=30

usage() {
  echo "Usage:" >&2
  echo "  $0 acquire <artifact-path> [timeout_seconds]" >&2
  echo "  $0 release <artifact-path>" >&2
  echo "  $0 check <artifact-path>" >&2
  exit 1
}

lock_path_for() {
  local artifact="$1"
  local basename
  basename="$(basename "$artifact")"
  echo "${LOCK_DIR}/${basename}.lock"
}

is_stale() {
  local lock_file="$1"
  if [[ ! -f "$lock_file" ]]; then
    return 1
  fi
  local lock_timestamp
  lock_timestamp="$(sed -n '2p' "$lock_file")"
  if [[ -z "$lock_timestamp" ]]; then
    return 0
  fi
  local now
  now="$(date +%s)"
  local age=$(( now - lock_timestamp ))
  if [[ "$age" -ge "$STALE_THRESHOLD_SECONDS" ]]; then
    return 0
  fi
  return 1
}

do_acquire() {
  local artifact="$1"
  local timeout="${2:-$DEFAULT_TIMEOUT}"
  local lock_file
  lock_file="$(lock_path_for "$artifact")"
  local agent_name="${HARNESS_AGENT_NAME:-unknown}"
  local pid="$$"
  local now

  mkdir -p "$LOCK_DIR"

  local elapsed=0
  while [[ "$elapsed" -lt "$timeout" ]]; do
    # Use mkdir for atomic creation. If it succeeds, we own the lock.
    if mkdir "${lock_file}.d" 2>/dev/null; then
      now="$(date +%s)"
      printf '%s\n%s\n%s\n' "$pid" "$now" "$agent_name" > "$lock_file"
      rmdir "${lock_file}.d"
      echo "Lock acquired: ${artifact} (pid=${pid}, agent=${agent_name})"
      return 0
    fi

    # Lock exists. Check for staleness.
    if is_stale "$lock_file"; then
      local old_holder
      old_holder="$(sed -n '3p' "$lock_file" 2>/dev/null || echo 'unknown')"
      echo "Overriding stale lock held by: ${old_holder}" >&2
      # Remove stale lock and retry immediately
      rm -f "$lock_file"
      rmdir "${lock_file}.d" 2>/dev/null || true
      continue
    fi

    sleep 1
    elapsed=$(( elapsed + 1 ))
  done

  local holder
  holder="$(sed -n '3p' "$lock_file" 2>/dev/null || echo 'unknown')"
  echo "ERROR: Timeout waiting for lock on ${artifact} (held by: ${holder})" >&2
  return 1
}

do_release() {
  local artifact="$1"
  local lock_file
  lock_file="$(lock_path_for "$artifact")"
  local pid="$$"

  if [[ ! -f "$lock_file" ]]; then
    echo "No lock to release: ${artifact}" >&2
    return 0
  fi

  local lock_pid
  lock_pid="$(sed -n '1p' "$lock_file")"

  if [[ "$lock_pid" != "$pid" ]]; then
    echo "WARNING: Lock on ${artifact} owned by pid ${lock_pid}, not ${pid}. Releasing anyway." >&2
  fi

  rm -f "$lock_file"
  echo "Lock released: ${artifact}"
  return 0
}

do_check() {
  local artifact="$1"
  local lock_file
  lock_file="$(lock_path_for "$artifact")"

  if [[ ! -f "$lock_file" ]]; then
    echo "Unlocked: ${artifact}"
    return 0
  fi

  if is_stale "$lock_file"; then
    echo "Stale lock (will be overridden): ${artifact}"
    return 0
  fi

  local lock_pid lock_timestamp lock_agent
  lock_pid="$(sed -n '1p' "$lock_file")"
  lock_timestamp="$(sed -n '2p' "$lock_file")"
  lock_agent="$(sed -n '3p' "$lock_file")"
  local now
  now="$(date +%s)"
  local age=$(( now - lock_timestamp ))

  echo "Locked: ${artifact} (pid=${lock_pid}, agent=${lock_agent}, age=${age}s)"
  return 1
}

# --- Main ---

if [[ $# -lt 2 ]]; then
  usage
fi

command="$1"
artifact="$2"
shift 2

case "$command" in
  acquire)
    do_acquire "$artifact" "$@"
    ;;
  release)
    do_release "$artifact"
    ;;
  check)
    do_check "$artifact"
    ;;
  *)
    usage
    ;;
esac
