"""Unit/smoke tests for fttp.config loading."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from fttp.config import FttpConfigError, load_config, resolve_config_path

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
