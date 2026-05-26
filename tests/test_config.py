"""Unit/smoke tests for fttp.config loading."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from fttp.config import (
    DEFAULT_WORKFLOW_PROFILE,
    DEFAULT_WRITING_MODE,
    FttpConfigError,
    load_config,
    resolve_config_path,
    validate_slug,
    workflow_profile,
    writing_mode,
)

REPO = Path(__file__).resolve().parents[1]


def _minimal_config(root: Path) -> dict:
    return {
        "workspaceName": "test-workspace",
        "repoRoot": str(root),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
    }


@pytest.mark.smoke
def test_resolve_prefers_fttp_config_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    (tmp_path / "workspace.config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "fttp.config.json").write_text("{}", encoding="utf-8")
    resolved = resolve_config_path()
    assert resolved is not None
    assert resolved.name == "fttp.config.json"


@pytest.mark.smoke
def test_resolve_fttp_config_env_override(tmp_path, monkeypatch):
    custom = tmp_path / "custom.config.json"
    custom.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("FTTP_CONFIG", str(custom))
    assert resolve_config_path() == custom.resolve()


@pytest.mark.smoke
def test_load_config_validates_required_fields(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    cfg_path = tmp_path / "fttp.config.json"
    cfg_path.write_text(json.dumps(_minimal_config(tmp_path)), encoding="utf-8")
    loaded = load_config()
    assert loaded["workspaceName"] == "test-workspace"
    assert loaded["_configPath"] == str(cfg_path.resolve())


@pytest.mark.smoke
def test_load_config_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    with pytest.raises(FttpConfigError, match="No workspace config found"):
        load_config()


@pytest.mark.smoke
def test_load_config_invalid_json_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    bad = tmp_path / "fttp.config.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(FttpConfigError, match="Invalid JSON"):
        load_config(bad)


@pytest.mark.smoke
def test_workflow_profile_and_writing_mode_defaults():
    cfg = {"workspaceName": "t", "repoRoot": "/tmp", "paper": {"dir": "paper", "mainTex": "main.tex"}}
    assert workflow_profile(cfg) == DEFAULT_WORKFLOW_PROFILE
    assert writing_mode(cfg) == DEFAULT_WRITING_MODE


@pytest.mark.smoke
def test_validate_slug_rejects_invalid():
    with pytest.raises(FttpConfigError, match="invalid"):
        validate_slug("Bad Slug!")
    with pytest.raises(FttpConfigError, match="invalid"):
        validate_slug("ab")


@pytest.mark.smoke
def test_validate_slug_accepts_canonical():
    validate_slug("my-thesis-workspace")


@pytest.mark.smoke
def test_load_config_rejects_invalid_workspace_slug(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    cfg = _minimal_config(tmp_path)
    cfg["workspaceSlug"] = "INVALID"
    (tmp_path / "fttp.config.json").write_text(json.dumps(cfg), encoding="utf-8")
    with pytest.raises(FttpConfigError, match="workspaceSlug"):
        load_config()


@pytest.mark.smoke
def test_load_config_rejects_read_only_root_inside_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    inner = tmp_path / "data" / "readonly"
    inner.mkdir(parents=True)
    cfg = _minimal_config(tmp_path)
    cfg["readOnlyRoots"] = ["data/readonly"]
    (tmp_path / "fttp.config.json").write_text(json.dumps(cfg), encoding="utf-8")
    with pytest.raises(FttpConfigError, match="readOnlyRoots"):
        load_config()


@pytest.mark.smoke
def test_load_config_rejects_invalid_workflow_profile(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    cfg = _minimal_config(tmp_path)
    cfg["workflowProfile"] = "thesis_only"
    (tmp_path / "fttp.config.json").write_text(json.dumps(cfg), encoding="utf-8")
    with pytest.raises(FttpConfigError, match="workflowProfile"):
        load_config()


@pytest.mark.smoke
def test_load_config_accepts_onboarding_v2_fields(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    cfg = _minimal_config(tmp_path)
    cfg.update(
        {
            "workspaceSlug": "test-workspace",
            "workflowProfile": "paper_only",
            "writingMode": "compose",
            "copyPolicy": {"maxArtifactMb": 100, "allowSymlinks": False},
        }
    )
    (tmp_path / "fttp.config.json").write_text(json.dumps(cfg), encoding="utf-8")
    loaded = load_config()
    assert loaded["workspaceSlug"] == "test-workspace"
    assert loaded["workflowProfile"] == "paper_only"
    assert loaded["writingMode"] == "compose"
