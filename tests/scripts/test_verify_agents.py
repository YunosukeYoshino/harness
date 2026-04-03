"""Tests for scripts/verify_agents.py."""
from __future__ import annotations

import subprocess
import sys
import textwrap

import pytest


SCRIPT = "scripts/verify_agents.py"


def run_script(cwd):
    """Run verify_agents.py from the given working directory."""
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


def _create_agent(tmp_repo, name: str, *, tools: str, skills: list[str]) -> None:
    """Create an agent .md file with valid frontmatter."""
    skills_yaml = "\n".join(f"  - {s}" for s in skills)
    content = textwrap.dedent(f"""\
        ---
        name: {name}
        tools: {tools}
        skills:
        {skills_yaml}
        ---
        # {name}
    """)
    path = tmp_repo / ".claude/agents" / f"{name}.md"
    path.write_text(content, encoding="utf-8")


def _create_skill(tmp_repo, skill_name: str) -> None:
    """Create a skill directory with SKILL.md."""
    skill_dir = tmp_repo / ".claude/skills" / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"# {skill_name}\n", encoding="utf-8")


class TestPassesWithValidAgents:
    """The script should pass with properly defined agents."""

    def test_passes_with_valid_agent(self, tmp_repo):
        _create_skill(tmp_repo, "my-skill")
        _create_agent(tmp_repo, "my-agent", tools="Read, Bash, Skill", skills=["my-skill"])

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()

    def test_passes_with_no_agents(self, tmp_repo):
        """When no agent files exist, there is nothing to validate."""
        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0


class TestFailsWithInvalidAgents:
    """The script should fail when agent definitions are invalid."""

    def test_fails_when_skill_tool_missing(self, tmp_repo):
        _create_skill(tmp_repo, "my-skill")
        _create_agent(tmp_repo, "bad-agent", tools="Read, Bash", skills=["my-skill"])

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "tools must include Skill" in result.stdout

    def test_fails_when_skills_list_empty(self, tmp_repo):
        agent_content = textwrap.dedent("""\
            ---
            name: no-skills-agent
            tools: Read, Bash, Skill
            ---
            # no-skills-agent
        """)
        (tmp_repo / ".claude/agents/no-skills-agent.md").write_text(
            agent_content, encoding="utf-8"
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "skills must be a non-empty list" in result.stdout

    def test_fails_when_referenced_skill_not_found(self, tmp_repo):
        _create_agent(
            tmp_repo, "orphan-agent",
            tools="Read, Bash, Skill",
            skills=["nonexistent-skill"],
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 1
        assert "referenced skill not found" in result.stdout


class TestToolGrantsFormat:
    """Validate that tools field is parsed correctly."""

    def test_multiple_tools_comma_separated(self, tmp_repo):
        _create_skill(tmp_repo, "test-skill")
        _create_agent(
            tmp_repo, "multi-tool-agent",
            tools="Read, Grep, Glob, Bash, Edit, Write, Skill",
            skills=["test-skill"],
        )

        _copy_script(tmp_repo)
        result = run_script(tmp_repo)

        assert result.returncode == 0
        assert "passed" in result.stdout.lower()
