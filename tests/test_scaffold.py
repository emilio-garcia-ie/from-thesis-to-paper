"""Tests for fttp scaffold command."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp.config import load_config
from fttp.scaffold import scaffold_workspace

REPO = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_scaffold_creates_workspace_with_slug(tmp_path):
    dest = scaffold_workspace("test-ws", tmp_path)
    assert dest == tmp_path / "test-ws"
    assert (dest / "README.md").is_file()
    assert (dest / "fttp.config.json").is_file()
    assert (dest / "paper" / "main.tex").is_file()

    readme = (dest / "README.md").read_text(encoding="utf-8")
    assert "{{WORKSPACE_SLUG}}" not in readme
    assert "test-ws" in readme

    cfg = json.loads((dest / "fttp.config.json").read_text(encoding="utf-8"))
    assert cfg["workspaceName"] == "test-ws"
    assert cfg["workspaceSlug"] == "test-ws"
    assert cfg["repoRoot"] == str(dest.resolve())
    assert "primary" in cfg["paper"]["venueProfiles"]


@pytest.mark.smoke
def test_scaffold_stub_hooks_allow_doctor(tmp_path, monkeypatch):
    dest = scaffold_workspace("doc-ws", tmp_path)
    cfg_path = dest / "fttp.config.json"
    monkeypatch.setenv("FTTP_CONFIG", str(cfg_path))
    monkeypatch.chdir(dest)

    loaded = load_config(cfg_path)
    assert loaded["workspaceSlug"] == "doc-ws"

    for rel in (loaded.get("hooks") or {}).values():
        assert (dest / rel).is_file(), f"missing hook stub: {rel}"

    from fttp.commands import cmd_doctor

    assert cmd_doctor(loaded) == 0


@pytest.mark.smoke
def test_scaffold_rejects_invalid_slug(tmp_path):
    with pytest.raises(Exception, match="invalid"):
        scaffold_workspace("BAD SLUG", tmp_path)


@pytest.mark.smoke
def test_scaffold_refuses_existing_dir(tmp_path):
    dest = tmp_path / "exists-ws"
    dest.mkdir()
    (dest / "marker.txt").write_text("x", encoding="utf-8")
    with pytest.raises(Exception, match="already exists"):
        scaffold_workspace("exists-ws", tmp_path)
