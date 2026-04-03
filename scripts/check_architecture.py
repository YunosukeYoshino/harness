#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config/architecture-boundaries.json").read_text(encoding="utf-8"))
IMPORT_RE = re.compile(r'from\s+["\'](@repo/[^"\']+)["\']|import\s+["\'](@repo/[^"\']+)["\']')

OWNERS = {
    "apps/web": "web",
    "apps/api": "api",
    "packages/domain": "domain",
    "packages/app": "app",
    "packages/data": "data",
    "packages/integrations": "integrations",
    "packages/ui": "ui",
    "packages/shared": "shared",
    "packages/schema": "schema",
}

def owner_for(path: pathlib.Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    for prefix, owner in OWNERS.items():
        if rel.startswith(prefix + "/"):
            return owner
    return None

violations: list[str] = []
for path in ROOT.rglob("*"):
    if path.suffix not in {".ts", ".tsx"}:
        continue
    if any(part in {"node_modules", "dist", "build", ".react-router"} for part in path.parts):
        continue
    owner = owner_for(path)
    if not owner:
        continue
    text = path.read_text(encoding="utf-8")
    for idx, line in enumerate(text.splitlines(), start=1):
        for match in IMPORT_RE.finditer(line):
            spec = match.group(1) or match.group(2)
            target = spec.split("/", 2)[1]
            allowed = set(CONFIG.get(owner, []))
            if target != owner and target not in allowed:
                violations.append(
                    f"{path.relative_to(ROOT)}:{idx}: {owner} cannot import {target}"
                )

if violations:
    print("Architecture boundary violations:")
    print("\n".join(violations))
    sys.exit(1)

print("Architecture boundary check passed.")
