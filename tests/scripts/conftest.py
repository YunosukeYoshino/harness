"""Shared fixtures for verification script tests."""
from __future__ import annotations

import pathlib
import shutil
import textwrap
from typing import Generator

import pytest


@pytest.fixture()
def tmp_repo(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create a minimal directory structure that mimics the repository layout.

    Returns the root path of the temporary repo.
    """
    dirs = [
        "work/plans/active",
        "work/sprint-contracts/active",
        "work/reviews/active",
        "work/qa-reports/active",
        "work/progress/current",
        "work/handoffs/active",
        ".claude/agents",
        ".claude/skills",
        "config",
        "scripts",
        "tests",
        "apps/web/src",
        "apps/api/src",
        "packages/domain/src",
        "packages/app/src",
        "packages/data/src",
        "packages/integrations/src",
        "packages/ui/src",
        "packages/shared/src",
        "packages/schema/src",
        "docs",
    ]
    for d in dirs:
        (tmp_path / d).mkdir(parents=True, exist_ok=True)

    return tmp_path


@pytest.fixture()
def make_plan(tmp_repo: pathlib.Path):
    """Factory fixture: creates a plan file under work/plans/active/."""

    def _make(slug: str, *, status: str = "in-progress") -> pathlib.Path:
        content = textwrap.dedent(f"""\
            ---
            title: {slug}
            status: {status}
            ---
            # {slug}

            ## Steps

            - Step 1: implement feature
        """)
        path = tmp_repo / "work/plans/active" / f"{slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    return _make


@pytest.fixture()
def make_progress(tmp_repo: pathlib.Path):
    """Factory fixture: creates a progress file under work/progress/current/."""

    def _make(slug: str) -> pathlib.Path:
        content = textwrap.dedent(f"""\
            ---
            title: {slug}
            ---
            # Progress: {slug}

            ## Done

            - Completed initial setup

            ## Next

            - Continue implementation

            ## Blockers

            - None
        """)
        path = tmp_repo / "work/progress/current" / f"{slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    return _make


@pytest.fixture()
def make_sprint_contract(tmp_repo: pathlib.Path):
    """Factory fixture: creates a sprint contract file."""

    def _make(slug: str) -> pathlib.Path:
        content = textwrap.dedent(f"""\
            ---
            title: {slug}
            ---
            # Sprint: {slug}

            ## Scope

            - Feature implementation

            ## Done

            - All tests pass
        """)
        path = tmp_repo / "work/sprint-contracts/active" / f"{slug}.md"
        path.write_text(content, encoding="utf-8")
        return path

    return _make


def make_artifact(base_dir: pathlib.Path, slug: str, *, artifact_type: str = "generic") -> pathlib.Path:
    """Helper: create a markdown artifact file with valid content for its type."""
    templates = {
        "review": f"""\
            ---
            title: {slug}
            ---
            # Review: {slug}

            ## Findings

            - No critical issues found
        """,
        "qa": f"""\
            ---
            title: {slug}
            ---
            # QA Report: {slug}

            ## Verdict

            PASS
        """,
        "handoff": f"""\
            ---
            title: {slug}
            ---
            # Handoff: {slug}

            ## Context

            - Feature implemented and tested

            ## Risks

            - None identified
        """,
        "generic": f"""\
            ---
            title: {slug}
            ---
            # {slug}
        """,
    }
    content = textwrap.dedent(templates.get(artifact_type, templates["generic"]))
    path = base_dir / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    return path
