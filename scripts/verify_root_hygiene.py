#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "config/root-hygiene.json").read_text(encoding="utf-8"))
allowed = set(config["allowed_root_markdown"])

violations = []
for path in ROOT.glob("*.md"):
    if path.name not in allowed:
        violations.append(path.name)

if violations:
    print("Unexpected markdown files in repository root:")
    for name in violations:
        print(f"- {name}")
    sys.exit(1)

print("Root hygiene check passed.")
