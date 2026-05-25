"""Schema validation for optional hooks and venueProfiles."""

from __future__ import annotations

import json

import pytest

from fttp.config import FttpConfigError, load_config, validate_hooks, validate_venue_profiles

from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.mark.smoke
def test_validate_hooks_rejects_absolute_path():
    cfg = {
        "workspaceName": "t",
        "repoRoot": "/tmp",
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "/abs/export.py"},
    }
    with pytest.raises(FttpConfigError, match="relative path"):
        validate_hooks(cfg)


@pytest.mark.smoke
def test_validate_hooks_rejects_unknown_key():
    cfg = {
        "workspaceName": "t",
        "repoRoot": "/tmp",
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"unknownHook": "scripts/x.py"},
    }
    with pytest.raises(FttpConfigError, match="unknown hook"):
        validate_hooks(cfg)


@pytest.mark.smoke
def test_validate_venue_active_must_exist(tmp_path):
    cfg = {
        "workspaceName": "t",
        "repoRoot": str(tmp_path),
        "paper": {
            "dir": "paper",
            "mainTex": "main.tex",
            "activeVenue": "missing",
            "venueProfiles": {"primary": {"mainTex": "main.tex"}},
        },
    }
    with pytest.raises(FttpConfigError, match="activeVenue"):
        validate_venue_profiles(cfg)


@pytest.mark.smoke
def test_load_config_with_hooks(tmp_path, monkeypatch):
    hook = FIXTURES / "hook_ok.py"
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "hook_ok.py").write_text(hook.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = {
        "workspaceName": "hook-test",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "scripts/hook_ok.py"},
    }

    path = tmp_path / "fttp.config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("FTTP_CONFIG", raising=False)
    loaded = load_config()
    assert loaded["hooks"]["tables"] == "scripts/hook_ok.py"
