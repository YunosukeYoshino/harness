#!/usr/bin/env bash
set -euo pipefail

api_pid=""
web_pid=""

cleanup() {
  if [[ -n "${web_pid}" ]]; then kill "${web_pid}" 2>/dev/null || true; fi
  if [[ -n "${api_pid}" ]]; then kill "${api_pid}" 2>/dev/null || true; fi
}
trap cleanup EXIT

wait_for_url() {
  local url="$1"
  local attempts="${2:-60}"
  local i=0
  until curl --silent --fail "$url" >/dev/null 2>&1; do
    i=$((i + 1))
    if [[ "$i" -ge "$attempts" ]]; then
      echo "Timed out waiting for $url" >&2
      exit 1
    fi
    sleep 1
  done
}

pnpm build:api >/dev/null
pnpm build:web >/dev/null

pnpm start:api >/tmp/agent-harness-api.log 2>&1 &
api_pid="$!"
wait_for_url "http://127.0.0.1:8787/health"

pnpm start:web >/tmp/agent-harness-web.log 2>&1 &
web_pid="$!"
wait_for_url "http://127.0.0.1:3000"

curl --silent --fail http://127.0.0.1:8787/health | grep '"status":"ok"' >/dev/null
curl --silent --fail http://127.0.0.1:3000 | grep 'Agent Harness Starter' >/dev/null

echo "runtime smoke passed"
