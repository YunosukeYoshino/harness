"""Tests for scripts/verify_root_hygiene.py."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest


SCRIPT = "scripts/verify_root_hygiene.py"


def run_script(cwd):
    """Run verify_root_hygiene.py from the given working directory."""
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


def _write_config(tmp_repo, allowed: list[str]) -> None:
    """Write root-hygiene.json config."""
    config_path = tmp_repo / "config/root-hygiene.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps({"allowed_root_markdown": allowed}),
        encoding="utf-8",
    )


class TestPassesWithAllowedFiles:
    """The script should pass when only allowed markdown files exist at root."""

    def test_passes_with_only_allowed_files(self, tmp_repo):
        allowed = ["README.md", "AGENTS.md", "CLAUDE.md", "SECURITY.md"]
        _write_config(tmp_repo, allowed)

        for name in allowed:
            (tmp_repo / name).write_text(f"# {name}\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_no_markdown_files(self, tmp_repo):
        _write_config(tmp_repo, ["README.md"])

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0


class TestFailsWithExtraFiles:
    """The script should fail when unexpected markdown files exist at root."""

    def test_fails_with_extra_markdown_file(self, tmp_repo):
        _write_config(tmp_repo, ["README.md"])
        (tmp_repo / "README.md").write_text("# README\n", encoding="utf-8")
        (tmp_repo / "NOTES.md").write_text("# Notes\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "NOTES.md" in result.stdout

    def test_fails_with_multiple_extra_files(self, tmp_repo):
        _write_config(tmp_repo, ["README.md"])
        (tmp_repo / "README.md").write_text("# README\n", encoding="utf-8")
        (tmp_repo / "EXTRA1.md").write_text("extra\n", encoding="utf-8")
        (tmp_repo / "EXTRA2.md").write_text("extra\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "EXTRA1.md" in result.stdout
        assert "EXTRA2.md" in result.stdout


class TestIgnoresNonMarkdown:
    """The script should not flag non-markdown files."""

    def test_ignores_non_markdown_files_at_root(self, tmp_repo):
        _write_config(tmp_repo, ["README.md"])

        (tmp_repo / "package.json").write_text("{}\n", encoding="utf-8")
        (tmp_repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        (tmp_repo / "Makefile").write_text("all:\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
