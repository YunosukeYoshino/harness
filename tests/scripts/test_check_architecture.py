"""Tests for scripts/check_architecture.py."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest


SCRIPT = "scripts/check_architecture.py"

DEFAULT_BOUNDARIES = {
    "web": ["ui", "shared", "schema", "domain"],
    "api": ["app", "domain", "shared", "schema", "data", "integrations"],
    "domain": ["shared", "schema"],
    "app": ["domain", "shared", "schema"],
    "data": ["domain", "shared", "schema"],
    "integrations": ["domain", "shared", "schema"],
    "ui": ["shared", "schema"],
    "shared": [],
    "schema": [],
}


def run_script(cwd):
    """Run check_architecture.py from the given working directory."""
    result = subprocess.run(
        [sys.executable, SCRIPT],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def _copy_script(tmp_repo):
    import shutil
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[2] / SCRIPT
    dst = tmp_repo / SCRIPT
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _write_boundaries(tmp_repo, boundaries: dict | None = None) -> None:
    """Write architecture-boundaries.json config."""
    config_path = tmp_repo / "config/architecture-boundaries.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(boundaries or DEFAULT_BOUNDARIES),
        encoding="utf-8",
    )


class TestPassesWithValidImports:
    """The script should pass when imports respect architecture boundaries."""

    def test_passes_when_no_source_files_exist(self, tmp_repo):
        _write_boundaries(tmp_repo)

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_allowed_import(self, tmp_repo):
        """packages/app is allowed to import packages/domain."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/app/src/service.ts"
        src_file.write_text(
            'import { User } from "@repo/domain/models";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_self_import(self, tmp_repo):
        """A package importing from itself should be fine (owner == target)."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/domain/src/index.ts"
        src_file.write_text(
            'import { Entity } from "@repo/domain/base";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0

    def test_passes_with_web_importing_ui(self, tmp_repo):
        """apps/web is allowed to import packages/ui."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "apps/web/src/page.tsx"
        src_file.write_text(
            'import { Button } from "@repo/ui/button";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0


class TestDetectsForbiddenImports:
    """The script should detect imports that violate architecture boundaries."""

    def test_detects_forbidden_import_app_to_ui(self, tmp_repo):
        """packages/app should NOT import packages/ui."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/app/src/handler.ts"
        src_file.write_text(
            'import { Button } from "@repo/ui/button";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "app cannot import ui" in result.stdout

    def test_detects_forbidden_import_shared_to_domain(self, tmp_repo):
        """packages/shared should NOT import packages/domain (empty allow list)."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/shared/src/util.ts"
        src_file.write_text(
            'import { User } from "@repo/domain/models";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "shared cannot import domain" in result.stdout

    def test_detects_forbidden_import_domain_to_data(self, tmp_repo):
        """packages/domain should NOT import packages/data."""
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/domain/src/entity.ts"
        src_file.write_text(
            'import { repo } from "@repo/data/repository";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "domain cannot import data" in result.stdout


class TestIgnoresIrrelevantFiles:
    """The script should skip files outside tracked packages and non-TS files."""

    def test_ignores_node_modules(self, tmp_repo):
        _write_boundaries(tmp_repo)

        nm_dir = tmp_repo / "packages/app/node_modules/@repo/ui"
        nm_dir.mkdir(parents=True, exist_ok=True)
        (nm_dir / "index.ts").write_text(
            'import { x } from "@repo/ui/internal";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0

    def test_ignores_non_ts_files(self, tmp_repo):
        _write_boundaries(tmp_repo)

        src_file = tmp_repo / "packages/shared/src/readme.md"
        src_file.write_text(
            'import { User } from "@repo/domain/models";\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
