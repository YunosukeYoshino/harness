#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / ".claude/agents"
SKILL_DIR = ROOT / ".claude/skills"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")

def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    data: dict[str, object] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for raw in lines:
        line = raw.rstrip()
        if not line:
            continue
        if ":" in line and not line.lstrip().startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                current_key = key
                current_list = []
                data[key] = current_list
            else:
                current_key = key
                current_list = None
                data[key] = value
        else:
            if current_list is not None:
                m = LIST_ITEM_RE.match(line)
                if m:
                    current_list.append(m.group(1))
    return data

violations: list[str] = []
for path in AGENT_DIR.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    tools = [part.strip() for part in str(fm.get("tools", "")).split(",") if part.strip()]
    skills = fm.get("skills", [])
    if "Skill" not in tools:
        violations.append(f"{path.relative_to(ROOT)}: tools must include Skill")
    if not isinstance(skills, list) or not skills:
        violations.append(f"{path.relative_to(ROOT)}: skills must be a non-empty list")
    else:
        for skill in skills:
            if not (SKILL_DIR / skill / "SKILL.md").exists():
                violations.append(
                    f"{path.relative_to(ROOT)}: referenced skill not found: {skill}"
                )

if violations:
    print("Agent definition check failed:")
    print("\n".join(violations))
    sys.exit(1)

print("Agent definition check passed.")
