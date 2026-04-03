#!/usr/bin/env python3
"""Verify harness state: artifact existence AND content validation."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "work/plans/active"
SPRINT_DIR = ROOT / "work/sprint-contracts/active"
REVIEW_DIR = ROOT / "work/reviews/active"
QA_DIR = ROOT / "work/qa-reports/active"
PROGRESS_DIR = ROOT / "work/progress/current"
HANDOFF_DIR = ROOT / "work/handoffs/active"

STATUS_RE = re.compile(r"^status:\s*(.+)$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
LIST_ITEM_RE = re.compile(r"^[ \t]*[-*]\s+\S", re.MULTILINE)
NO_FINDINGS_RE = re.compile(r"no\s+findings", re.IGNORECASE)


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- ... ---) from the beginning of text."""
    return FRONTMATTER_RE.sub("", text)


def _section_body(body: str, heading: str) -> str | None:
    """Extract the text between a given ## heading and the next ## heading (or EOF).

    Returns None if the heading does not exist.
    """
    pattern = re.compile(
        r"^##\s+" + re.escape(heading) + r"\s*\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    if match is None:
        return None
    return match.group(1)


def _has_list_item(section_text: str) -> bool:
    """Return True if the section contains at least one markdown list item."""
    return LIST_ITEM_RE.search(section_text) is not None


def _find_any_heading(body: str, candidates: list[str]) -> str | None:
    """Return the first heading name from *candidates* that exists in *body*, or None."""
    for heading in candidates:
        if _section_body(body, heading) is not None:
            return heading
    return None


# -- per-type validators -----------------------------------------------------

def _validate_plan(filepath: pathlib.Path, body: str) -> list[str]:
    """Plans must have '## Steps' or '## Tasks' with at least 1 list item."""
    issues: list[str] = []
    heading = _find_any_heading(body, ["Steps", "Tasks"])
    if heading is None:
        issues.append(
            f"CONTENT_VIOLATION: plan '{filepath.name}' missing "
            "'## Steps' or '## Tasks' section"
        )
        return issues
    section = _section_body(body, heading)
    if section is not None and not _has_list_item(section):
        issues.append(
            f"CONTENT_VIOLATION: plan '{filepath.name}' "
            f"'## {heading}' section has no list items"
        )
    return issues


def _validate_sprint(filepath: pathlib.Path, body: str) -> list[str]:
    """Sprint contracts must have '## Scope' and '## Done' sections."""
    issues: list[str] = []
    # Accept common variants for the "Done" heading
    for required, alts in [
        ("Scope", ["Scope", "Deliverables"]),
        ("Done", ["Done", "Done definition"]),
    ]:
        found = _find_any_heading(body, alts)
        if found is None:
            issues.append(
                f"CONTENT_VIOLATION: sprint contract '{filepath.name}' "
                f"missing '## {required}' section"
            )
    return issues


def _validate_progress(filepath: pathlib.Path, body: str) -> list[str]:
    """Progress must have '## Done', '## Next', '## Blockers'; Done needs 1 item."""
    issues: list[str] = []
    for heading in ["Done", "Next", "Blockers"]:
        if _section_body(body, heading) is None:
            issues.append(
                f"CONTENT_VIOLATION: progress '{filepath.name}' "
                f"missing '## {heading}' section"
            )
    done_section = _section_body(body, "Done")
    if done_section is not None and not _has_list_item(done_section):
        issues.append(
            f"CONTENT_VIOLATION: progress '{filepath.name}' "
            "'## Done' section has no list items"
        )
    return issues


def _validate_qa(filepath: pathlib.Path, body: str) -> list[str]:
    """QA reports must have '## Verdict' or '## Result' section."""
    issues: list[str] = []
    if _find_any_heading(body, ["Verdict", "Result"]) is None:
        issues.append(
            f"CONTENT_VIOLATION: QA report '{filepath.name}' "
            "missing '## Verdict' or '## Result' section"
        )
    return issues


def _validate_handoff(filepath: pathlib.Path, body: str) -> list[str]:
    """Handoffs must have '## Risks' or '## Context' section."""
    issues: list[str] = []
    if _find_any_heading(body, ["Risks", "Context"]) is None:
        issues.append(
            f"CONTENT_VIOLATION: handoff '{filepath.name}' "
            "missing '## Risks' or '## Context' section"
        )
    return issues


def _validate_review(filepath: pathlib.Path, body: str) -> list[str]:
    """Reviews must have findings or a 'no findings' statement."""
    issues: list[str] = []
    # Accept any heading that indicates findings (e.g. "Codex findings", "Findings", "Triage")
    has_findings_heading = _find_any_heading(
        body, ["Codex findings", "Findings", "Triage", "Fixes"]
    )
    has_no_findings_stmt = NO_FINDINGS_RE.search(body) is not None

    if has_findings_heading is not None:
        section = _section_body(body, has_findings_heading)
        if section is not None and _has_list_item(section):
            return issues
    if has_no_findings_stmt:
        return issues

    # Neither findings items nor a "no findings" statement
    issues.append(
        f"CONTENT_VIOLATION: review '{filepath.name}' "
        "missing findings or 'no findings' statement"
    )
    return issues


_VALIDATORS = {
    "plan": _validate_plan,
    "sprint": _validate_sprint,
    "progress": _validate_progress,
    "qa": _validate_qa,
    "handoff": _validate_handoff,
    "review": _validate_review,
}


def validate_artifact_content(
    filepath: pathlib.Path, artifact_type: str
) -> list[str]:
    """Read *filepath*, strip frontmatter, and run the type-specific validator.

    Returns a list of violation strings (empty means valid).
    """
    validator = _VALIDATORS.get(artifact_type)
    if validator is None:
        return [f"Unknown artifact type: {artifact_type}"]

    text = filepath.read_text(encoding="utf-8")
    body = strip_frontmatter(text)
    return validator(filepath, body)


# -- main --------------------------------------------------------------------

plans = sorted(p for p in PLAN_DIR.glob("*.md") if p.is_file())
if not plans:
    print("Harness state check passed: no active work item.")
    sys.exit(0)

violations: list[str] = []
for plan in plans:
    slug = plan.stem
    text = plan.read_text(encoding="utf-8")
    status_match = STATUS_RE.search(text)
    status = status_match.group(1).strip().lower() if status_match else "draft"

    # -- existence checks (unchanged) ----------------------------------------
    required_always: list[tuple[pathlib.Path, str]] = [
        (SPRINT_DIR / f"{slug}.md", "sprint"),
        (PROGRESS_DIR / f"{slug}.md", "progress"),
    ]
    for path, _ in required_always:
        if not path.exists():
            violations.append(f"Missing required artifact: {path.relative_to(ROOT)}")

    if status in {"ready-for-review", "ready-for-stop", "done", "complete"}:
        required_at_completion: list[tuple[pathlib.Path, str]] = [
            (REVIEW_DIR / f"{slug}.md", "review"),
            (QA_DIR / f"{slug}.md", "qa"),
            (HANDOFF_DIR / f"{slug}.md", "handoff"),
        ]
        for path, _ in required_at_completion:
            if not path.exists():
                violations.append(
                    f"Missing completion artifact: {path.relative_to(ROOT)}"
                )
    else:
        required_at_completion = []

    # -- content checks (new) ------------------------------------------------
    # Validate the plan itself
    violations.extend(validate_artifact_content(plan, "plan"))

    # Validate companion artifacts that exist
    all_artifacts = required_always + required_at_completion
    for path, artifact_type in all_artifacts:
        if path.exists():
            violations.extend(validate_artifact_content(path, artifact_type))

if violations:
    print("Harness state check failed:")
    for v in violations:
        print(f"  {v}")
    sys.exit(1)

print("Harness state check passed.")
