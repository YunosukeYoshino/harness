#!/usr/bin/env python3
"""Verify that every route defined in the web app has at least one E2E test.

Scans route definitions in apps/web/app/routes.ts (and the routes/ directory)
and compares them against test files in tests/e2e/.

Exit 0 if all routes are covered (or routes dir does not exist yet).
Exit 1 if coverage gaps are found.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROUTES_FILE = ROOT / "apps" / "web" / "app" / "routes.ts"
ROUTES_DIR = ROOT / "apps" / "web" / "app" / "routes"
E2E_DIR = ROOT / "tests" / "e2e"

# Matches React Router route helpers like: index("./routes/_index.tsx")
# or route("about", "./routes/about.tsx")
ROUTE_CALL_RE = re.compile(
    r"""(?:index|route)\(\s*(?:["']([^"']+)["']\s*,\s*)?["']([^"']+)["']""",
)

# Matches imports/references to route paths inside test files
# e.g. page.goto("/about")  or  request.get("http://127.0.0.1:8787/health")
GOTO_RE = re.compile(r"""(?:goto|get|post|put|delete)\(\s*["'](?:https?://[^/]*)?(/[^"']*)["']""")


def extract_routes_from_config(path: pathlib.Path) -> list[str]:
    """Parse routes.ts for route path strings."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    routes: list[str] = []
    for match in ROUTE_CALL_RE.finditer(text):
        route_path = match.group(1)  # First arg (path string) or None for index
        file_ref = match.group(2)    # File reference
        if route_path is not None:
            routes.append("/" + route_path.strip("/"))
        else:
            # index() routes map to "/"
            routes.append("/")
    return routes


def extract_routes_from_directory(routes_dir: pathlib.Path) -> list[str]:
    """Derive route paths from file-system route files."""
    if not routes_dir.exists():
        return []
    routes: list[str] = []
    for file in sorted(routes_dir.glob("**/*.tsx")):
        relative = file.relative_to(routes_dir)
        stem = str(relative.with_suffix(""))
        # Convert _index to /
        if stem == "_index":
            routes.append("/")
            continue
        # Strip leading underscore prefix used for layout routes
        cleaned = stem.replace("_index", "").strip("/")
        if cleaned:
            # Convert dots and underscores to slashes where appropriate
            route_path = "/" + cleaned.replace(".", "/")
            routes.append(route_path)
    return routes


def extract_tested_paths(e2e_dir: pathlib.Path) -> set[str]:
    """Scan E2E test files for navigated paths."""
    paths: set[str] = set()
    if not e2e_dir.exists():
        return paths
    for file in e2e_dir.glob("**/*.spec.ts"):
        text = file.read_text(encoding="utf-8")
        for match in GOTO_RE.finditer(text):
            raw_path = match.group(1)
            # Normalize: strip trailing slash, default empty to /
            normalized = raw_path.rstrip("/") or "/"
            paths.add(normalized)
    return paths


def main() -> int:
    # Handle case where routes infrastructure does not exist yet
    if not ROUTES_FILE.exists() and not ROUTES_DIR.exists():
        print("PASS (with warning): No routes file or directory found.")
        print("  Expected: apps/web/app/routes.ts or apps/web/app/routes/")
        print("  This is acceptable for a fresh project.")
        return 0

    # Collect all defined routes (deduplicated)
    defined_routes: set[str] = set()
    defined_routes.update(extract_routes_from_config(ROUTES_FILE))
    defined_routes.update(extract_routes_from_directory(ROUTES_DIR))

    if not defined_routes:
        print("PASS (with warning): No route definitions found to verify.")
        return 0

    # Collect tested paths
    tested_paths = extract_tested_paths(E2E_DIR)

    # Compare
    uncovered = sorted(defined_routes - tested_paths)

    print(f"Defined routes:  {sorted(defined_routes)}")
    print(f"Tested paths:    {sorted(tested_paths)}")
    print()

    if uncovered:
        print(f"FAIL: {len(uncovered)} route(s) without E2E coverage:")
        for route in uncovered:
            print(f"  - {route}")
        print()
        print("Add E2E tests in tests/e2e/ that navigate to these routes.")
        return 1

    print(f"PASS: All {len(defined_routes)} route(s) have E2E coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
