"""First-use tests for the guided consumer workspace commands."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "python")
    env.pop("FTTP_CONFIG", None)
    return subprocess.run(
        [sys.executable, "-m", "fttp", *args], cwd=cwd, env=env,
        text=True, capture_output=True, check=False,
    )


@pytest.mark.smoke
@pytest.mark.parametrize(
    ("agent", "entry", "skill_root"),
    [
        ("cursor", ".cursor/rules/fttp-workspace.mdc", ".cursor/skills"),
        ("claude", "CLAUDE.md", ".claude/skills"),
        ("codex", "AGENTS.md", ".agents/skills"),
    ],
)
def test_init_creates_selected_agent_and_self_contained_intake(tmp_path, agent, entry, skill_root):
    workspace = tmp_path / f"paper-{agent}"
    result = _run(tmp_path, "init", str(workspace), "--agent", agent)
    assert result.returncode == 0, result.stderr
    cfg = json.loads((workspace / "fttp.config.json").read_text(encoding="utf-8"))
    assert cfg["agentStack"] == agent
    assert cfg["readOnlyRoots"] == []
    assert (workspace / entry).is_file()
    assert (workspace / skill_root / "agent-intake" / "SKILL.md").is_file()
    assert not (workspace / ".cursor" / "skills").exists() or agent == "cursor"
    assert (workspace / "GETTING_STARTED.md").is_file()
    assert (workspace / ".fttp" / "guides" / "ONBOARDING_RATIONALE.md").is_file()
    intake = workspace / skill_root / "agent-intake" / "SKILL.md"
    assert "](../../../.fttp/guides/WORKSPACE_MODEL.md)" in intake.read_text(encoding="utf-8")
    assert (intake.parent / "../../../.fttp/guides/WORKSPACE_MODEL.md").resolve().is_file()
    manifest = json.loads((workspace / ".fttp" / "resource-manifest.json").read_text())
    assert manifest["agent"] == agent
    assert all(not Path(path).is_absolute() for path in manifest["files"])


@pytest.mark.smoke
def test_start_and_status_are_read_only_reports(tmp_path):
    workspace = tmp_path / "paper-status"
    assert _run(tmp_path, "init", str(workspace), "--agent", "codex").returncode == 0
    before = (workspace / "GETTING_STARTED.md").read_bytes()
    start = _run(workspace, "start")
    status = _run(workspace, "status")
    assert start.returncode == status.returncode == 0
    assert "prompt:" in start.stdout
    assert "not a manuscript readiness certificate" in status.stdout
    assert (workspace / "GETTING_STARTED.md").read_bytes() == before


@pytest.mark.smoke
def test_init_refuses_occupied_destination_without_overwriting(tmp_path):
    workspace = tmp_path / "occupied-paper"
    workspace.mkdir()
    marker = workspace / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    result = _run(tmp_path, "init", str(workspace), "--agent", "codex")
    assert result.returncode == 1
    assert marker.read_text(encoding="utf-8") == "keep"


@pytest.mark.smoke
def test_init_requires_agent_when_stdin_is_not_interactive(tmp_path):
    result = _run(tmp_path, "init", str(tmp_path / "paper"))
    assert result.returncode == 1
    assert "--agent is required" in result.stderr
