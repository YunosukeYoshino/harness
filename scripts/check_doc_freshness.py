#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "config/doc-freshness.json").read_text(encoding="utf-8"))

required = config["required_frontmatter_keys"]
violations: list[str] = []

for pattern in config["globs"]:
    for path in ROOT.glob(pattern):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            violations.append(f"{path.relative_to(ROOT)}: missing frontmatter")
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            violations.append(f"{path.relative_to(ROOT)}: malformed frontmatter")
            continue
        frontmatter = parts[1]
        for key in required:
            if f"{key}:" not in frontmatter:
                violations.append(f"{path.relative_to(ROOT)}: missing {key}")

if violations:
    print("Documentation freshness check failed:")
    print("\n".join(violations))
    sys.exit(1)

print("Documentation freshness check passed.")
