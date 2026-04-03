#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"\b(?:test|it|describe)\.skip\s*\(")
TARGETS = [ROOT / "tests", ROOT / "apps", ROOT / "packages"]

hits: list[str] = []
for base in TARGETS:
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if path.suffix not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        text = path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            if PATTERN.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{idx}: {line.strip()}")

if hits:
    print("Skipped tests are not allowed:")
    print("\n".join(hits))
    sys.exit(1)

print("No skipped tests found.")
