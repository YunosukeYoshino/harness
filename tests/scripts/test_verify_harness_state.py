"""Tests for scripts/verify_harness_state.py."""
from __future__ import annotations

import subprocess
import sys
import textwrap

import pytest


SCRIPT = "scripts/verify_harness_state.py"


def run_script(cwd):
    """Run verify_harness_state.py from the given working directory."""
    result = subprocess.run(
        [sys.executable, SCRIPT],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


class TestPassesWithAllArtifacts:
    """The script should pass when all required artifacts exist."""

    def test_passes_with_valid_in_progress_artifacts(self, tmp_repo, make_plan, make_sprint_contract, make_progress):
        slug = "feature-x"
        make_plan(slug, status="in-progress")
        make_sprint_contract(slug)
        make_progress(slug)

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_completion_artifacts(self, tmp_repo, make_plan, make_sprint_contract, make_progress):
        from conftest import make_artifact

        slug = "feature-y"
        make_plan(slug, status="done")
        make_sprint_contract(slug)
        make_progress(slug)
        make_artifact(tmp_repo / "work/reviews/active", slug, artifact_type="review")
        make_artifact(tmp_repo / "work/qa-reports/active", slug, artifact_type="qa")
        make_artifact(tmp_repo / "work/handoffs/active", slug, artifact_type="handoff")

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()


class TestFailsWhenArtifactsMissing:
    """The script should fail when required artifacts are missing."""

    def test_fails_when_progress_missing(self, tmp_repo, make_plan, make_sprint_contract):
        slug = "feature-z"
        make_plan(slug)
        make_sprint_contract(slug)
        # progress is NOT created

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Missing required artifact" in result.stdout

    def test_fails_when_sprint_contract_missing(self, tmp_repo, make_plan, make_progress):
        slug = "feature-w"
        make_plan(slug)
        make_progress(slug)
        # sprint contract is NOT created

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Missing required artifact" in result.stdout

    def test_fails_when_completion_artifacts_missing_for_done_status(
        self, tmp_repo, make_plan, make_sprint_contract, make_progress
    ):
        slug = "feature-done"
        make_plan(slug, status="done")
        make_sprint_contract(slug)
        make_progress(slug)
        # review, qa-report, handoff are NOT created

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "Missing completion artifact" in result.stdout


class TestEdgeCases:
    """Edge cases and special scenarios."""

    def test_passes_when_no_active_plans_exist(self, tmp_repo):
        """When no plan files exist, the script reports no active work and passes."""
        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "no active work item" in result.stdout.lower()

    def test_gitkeep_only_passes(self, tmp_repo):
        """A .gitkeep file is not a .md plan, so the script should pass (no plans found)."""
        (tmp_repo / "work/plans/active/.gitkeep").touch()

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "no active work item" in result.stdout.lower()

    def test_handles_malformed_yaml_frontmatter(self, tmp_repo, make_sprint_contract, make_progress):
        """When a plan file has no status in frontmatter, it defaults to 'draft'.
        Content validation still applies, so we include required sections."""
        slug = "malformed"
        plan_path = tmp_repo / "work/plans/active" / f"{slug}.md"
        plan_path.write_text("No frontmatter here, just text.\n\n## Steps\n\n- Step 1\n", encoding="utf-8")
        make_sprint_contract(slug)
        make_progress(slug)

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        # status defaults to "draft", which is not a completion status,
        # so only sprint + progress are required (both present) -> pass
        assert result.returncode == 0


def _copy_script(tmp_repo):
    """Copy the verification script into the tmp repo so ROOT resolves correctly."""
    import shutil
    src = _project_root() / SCRIPT
    dst = tmp_repo / SCRIPT
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _project_root():
    import pathlib
    return pathlib.Path(__file__).resolve().parents[2]
