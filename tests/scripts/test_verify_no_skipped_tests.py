"""Tests for scripts/verify_no_skipped_tests.py."""
from __future__ import annotations

import subprocess
import sys

import pytest


SCRIPT = "scripts/verify_no_skipped_tests.py"


def run_script(cwd):
    """Run verify_no_skipped_tests.py from the given working directory."""
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


class TestPassesWithCleanFiles:
    """The script should pass when no skip patterns are present."""

    def test_passes_with_clean_test_files(self, tmp_repo):
        test_file = tmp_repo / "tests" / "example.test.ts"
        test_file.write_text(
            'test("adds numbers", () => {\n  expect(1 + 1).toBe(2);\n});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "No skipped tests found" in result.stdout

    def test_passes_with_no_test_files(self, tmp_repo):
        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0


class TestDetectsSkipPatterns:
    """The script should detect various .skip patterns."""

    def test_detects_test_skip(self, tmp_repo):
        test_file = tmp_repo / "tests" / "example.test.ts"
        test_file.write_text(
            'test.skip("should not be here", () => {});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Skipped tests are not allowed" in result.stdout

    def test_detects_it_skip(self, tmp_repo):
        test_file = tmp_repo / "tests" / "example.test.tsx"
        test_file.write_text(
            'it.skip("should not be here", () => {});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Skipped tests are not allowed" in result.stdout

    def test_detects_describe_skip(self, tmp_repo):
        test_file = tmp_repo / "tests" / "example.test.js"
        test_file.write_text(
            'describe.skip("suite", () => {\n  it("test", () => {});\n});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Skipped tests are not allowed" in result.stdout

    def test_detects_skip_in_apps_directory(self, tmp_repo):
        test_file = tmp_repo / "apps" / "web" / "src" / "component.test.tsx"
        test_file.write_text(
            'test.skip("broken", () => {});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1

    def test_detects_skip_in_packages_directory(self, tmp_repo):
        test_file = tmp_repo / "packages" / "domain" / "src" / "logic.test.ts"
        test_file.write_text(
            'it.skip("todo", () => {});\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1


class TestIgnoresNonTargetFiles:
    """The script should ignore skip patterns in non-test file types."""

    def test_ignores_skip_in_python_files(self, tmp_repo):
        py_file = tmp_repo / "tests" / "test_example.py"
        py_file.write_text(
            'test.skip("this is python, should be ignored")\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0

    def test_ignores_skip_in_markdown_files(self, tmp_repo):
        md_file = tmp_repo / "tests" / "notes.md"
        md_file.write_text(
            'Example: test.skip("demo")\n',
            encoding="utf-8",
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
