#!/usr/bin/env bash
set -euo pipefail

# Install upstream skills for the agent harness
# These are optional skills that enhance agent capabilities for specific tech stacks
#
# Usage:
#   bash tools/install-upstream-skills.sh          Install all upstream skills
#   bash tools/install-upstream-skills.sh --list    List available skills without installing
#   bash tools/install-upstream-skills.sh --help    Show usage information

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.claude/skills"
AGENTS_SKILLS_DIR="$REPO_ROOT/.agents/skills"

# ---------------------------------------------------------------------------
# Upstream skill registry
# Each entry: "skill-name|source|description"
# Skills are installed project-locally into .claude/skills/ via `npx skills add`.
# ---------------------------------------------------------------------------
SKILLS=(
  "react-router-framework-mode|remix-run/agent-skills|React Router framework mode skill (loaders, actions, route modules)"
  "hono|yusukebe/hono-skill|Hono skill (routing, middleware, validation, testing)"
  "shadcn|shadcn/ui|shadcn/ui component generation skill"
  "ai-elements|vercel/ai-elements|Vercel AI Elements skill"
  "prisma-client-api|prisma/skills|Prisma Client API skill"
  "agent-browser|vercel-labs/agent-browser|agent-browser visual verification skill"
  "design-taste-frontend|https://github.com/Leonxlnx/taste-skill|Taste Skill frontend design guidance"
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

usage() {
  cat <<'USAGE'
Usage: bash tools/install-upstream-skills.sh [OPTIONS]

Install upstream skills into this project's agent skill directories

Options:
  --list    List available skills without installing
  --help    Show this help message

Skills are installed with `npx skills add` as project-local dependencies.
The skills CLI stores installed packages under `.agents/skills/`. This script
ensures `.claude/skills/<skill-name>` is a symlink to the corresponding
`.agents/skills/<skill-name>` directory. Each installed skill is validated to
contain a SKILL.md file at `.claude/skills/<skill-name>/SKILL.md`.
The script is idempotent -- running it multiple times is safe.

Environment:
  SKIP_NPX_INSTALL=1    Skip install commands (useful for offline/testing)
USAGE
}

list_skills() {
  printf "%-20s  %s\n" "NAME" "DESCRIPTION"
  printf "%-20s  %s\n" "----" "-----------"
  for entry in "${SKILLS[@]}"; do
    IFS='|' read -r name source description <<< "$entry"
    printf "%-20s  %s\n" "$name" "$description"
  done
}

install_skill_via_npx() {
  local name="$1"
  local source="$2"

  if [[ "${SKIP_NPX_INSTALL:-0}" == "1" ]]; then
    echo "  [skip] $name -- install command skipped by SKIP_NPX_INSTALL=1"
    return 2
  fi

  echo "  [install] $name from $source"
  if (
    cd "$REPO_ROOT"
    npx skills add "$source" --agent claude-code --skill "$name" -y
  ); then
    return 0
  fi

  echo "  [warn] $name -- install failed"
  return 1
}

validate_skill() {
  local name="$1"
  local skill_dir="$SKILLS_DIR/$name"

  if [[ -f "$skill_dir/SKILL.md" ]]; then
    echo "  [ok] $name -- SKILL.md present"
    return 0
  else
    echo "  [warn] $name -- SKILL.md missing after install"
    return 1
  fi
}

relink_skill() {
  local name="$1"
  local agent_skill_dir="$AGENTS_SKILLS_DIR/$name"
  local claude_skill_dir="$SKILLS_DIR/$name"
  local expected_link="../../.agents/skills/$name"

  if [[ ! -d "$agent_skill_dir" ]]; then
    echo "  [warn] $name -- installed package not found under .agents/skills"
    return 1
  fi

  if [[ -L "$claude_skill_dir" ]] && [[ "$(readlink "$claude_skill_dir")" == "$expected_link" ]]; then
    return 0
  fi

  if [[ -e "$claude_skill_dir" || -L "$claude_skill_dir" ]]; then
    /usr/bin/trash "$claude_skill_dir"
  fi

  ln -s "$expected_link" "$claude_skill_dir"
  echo "  [link] $name -- .claude/skills now points to .agents/skills"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
  case "${1:-}" in
    --help|-h)
      usage
      exit 0
      ;;
    --list|-l)
      list_skills
      exit 0
      ;;
    "")
      # default: install
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac

  echo "=== Upstream Skills Installer ==="
  echo ""
  echo "Package directory: $AGENTS_SKILLS_DIR"
  echo "Claude directory:  $SKILLS_DIR"
  echo ""

  mkdir -p "$AGENTS_SKILLS_DIR"
  mkdir -p "$SKILLS_DIR"

  local installed=0
  local skipped=0
  local failed=0

  for entry in "${SKILLS[@]}"; do
    IFS='|' read -r name source description <<< "$entry"
    echo "--- $name ---"

    if install_skill_via_npx "$name" "$source"; then
      status=0
    else
      status=$?
    fi

    if [[ $status -ne 0 ]]; then
      if [[ $status -eq 2 ]]; then
        skipped=$((skipped + 1))
      else
        failed=$((failed + 1))
      fi
      echo ""
      continue
    fi

    if ! relink_skill "$name"; then
      failed=$((failed + 1))
      echo ""
      continue
    fi

    # Validate
    if validate_skill "$name"; then
      installed=$((installed + 1))
    else
      failed=$((failed + 1))
    fi

    echo ""
  done

  echo "=== Summary ==="
  echo "Installed: $installed"
  echo "Skipped:   $skipped"
  echo "Failed:    $failed"
  echo ""

  if [[ $failed -gt 0 ]]; then
    echo "Some skills failed validation. Check output above."
  fi

  cat <<'NEXT'
Suggested next steps:
- Commit the resulting project-local skill changes if you want them versioned
- Restart Claude Code after installing upstream skills
- See docs/stack-profiles/ui-and-skills.md for skill usage guidance
NEXT
}

main "$@"
