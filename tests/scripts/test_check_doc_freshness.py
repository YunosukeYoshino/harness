"""Tests for scripts/check_doc_freshness.py."""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap

import pytest


SCRIPT = "scripts/check_doc_freshness.py"


def run_script(cwd):
    """Run check_doc_freshness.py from the given working directory."""
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


def _write_config(tmp_repo, *, globs: list[str] | None = None, keys: list[str] | None = None) -> None:
    """Write doc-freshness.json config."""
    config_path = tmp_repo / "config/doc-freshness.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps({
            "globs": globs or ["docs/**/*.md"],
            "required_frontmatter_keys": keys or ["title", "last-reviewed"],
        }),
        encoding="utf-8",
    )


class TestPassesWithValidFrontmatter:
    """The script should pass when docs have valid frontmatter."""

    def test_passes_with_complete_frontmatter(self, tmp_repo):
        _write_config(tmp_repo)

        doc = tmp_repo / "docs" / "guide.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            textwrap.dedent("""\
                ---
                title: Guide
                last-reviewed: 2026-03-01
                ---
                # Guide
            """),
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_no_doc_files(self, tmp_repo):
        _write_config(tmp_repo)

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0


class TestFailsWithMissingKeys:
    """The script should fail when required frontmatter keys are missing."""

    def test_fails_when_title_missing(self, tmp_repo):
        _write_config(tmp_repo)

        doc = tmp_repo / "docs" / "guide.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            textwrap.dedent("""\
                ---
                last-reviewed: 2026-03-01
                ---
                # Guide
            """),
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "missing title" in result.stdout

    def test_fails_when_last_reviewed_missing(self, tmp_repo):
        _write_config(tmp_repo)

        doc = tmp_repo / "docs" / "guide.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            textwrap.dedent("""\
                ---
                title: Guide
                ---
                # Guide
            """),
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "missing last-reviewed" in result.stdout

    def test_fails_when_no_frontmatter_at_all(self, tmp_repo):
        _write_config(tmp_repo)

        doc = tmp_repo / "docs" / "bare.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("# Just a heading\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "missing frontmatter" in result.stdout

    def test_fails_with_malformed_frontmatter(self, tmp_repo):
        _write_config(tmp_repo)

        doc = tmp_repo / "docs" / "broken.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        # Only opening --- but no closing ---
        doc.write_text("---\ntitle: Broken\n# Content\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "malformed frontmatter" in result.stdout


class TestIgnoresFilesNotInConfig:
    """The script should only check files matching the configured globs."""

    def test_ignores_files_outside_docs(self, tmp_repo):
        _write_config(tmp_repo, globs=["docs/**/*.md"])

        # This file is at root, not under docs/
        (tmp_repo / "README.md").write_text("# No frontmatter\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0

    def test_ignores_non_matching_glob(self, tmp_repo):
        _write_config(tmp_repo, globs=["docs/architecture/**/*.md"])

        # This file is under docs/ but not docs/architecture/
        other_doc = tmp_repo / "docs" / "guide.md"
        other_doc.parent.mkdir(parents=True, exist_ok=True)
        other_doc.write_text("# No frontmatter\n", encoding="utf-8")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0

    def test_checks_nested_docs(self, tmp_repo):
        _write_config(tmp_repo, globs=["docs/**/*.md"])

        nested_doc = tmp_repo / "docs" / "architecture" / "overview.md"
        nested_doc.parent.mkdir(parents=True, exist_ok=True)
        nested_doc.write_text(
            textwrap.dedent("""\
                ---
                title: Overview
                last-reviewed: 2026-03-01
                ---
                # Overview
            """),
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
