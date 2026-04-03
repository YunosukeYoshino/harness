"""Tests for scripts/new-work-item.sh."""
from __future__ import annotations

import pathlib
import subprocess


SCRIPT = "scripts/new-work-item.sh"


def _project_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[2]


def _copy_script(tmp_repo: pathlib.Path) -> None:
    import shutil

    src = _project_root() / SCRIPT
    dst = tmp_repo / SCRIPT
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def test_new_work_item_scaffolds_spec_artifacts(tmp_repo: pathlib.Path) -> None:
    slug = "feature-spec-first"
    _copy_script(tmp_repo)

    result = subprocess.run(
        ["bash", SCRIPT, slug],
        cwd=tmp_repo,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert (tmp_repo / f"work/specs/active/{slug}.prompt.md").exists()
    assert (tmp_repo / f"work/specs/active/{slug}.md").exists()
    assert (tmp_repo / f"work/plans/active/{slug}.md").exists()
    assert (tmp_repo / f"work/sprint-contracts/active/{slug}.md").exists()

    spec_text = (tmp_repo / f"work/specs/active/{slug}.md").read_text(encoding="utf-8")
    assert "## Goal" in spec_text
    assert "## Repo Constraints" in spec_text
