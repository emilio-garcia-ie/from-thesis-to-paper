"""Subprocess hook delegation tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp.commands import run_hook

REPO = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _cfg_with_hooks(tmp_path: Path, hook_name: str, script_name: str) -> dict:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    src = FIXTURES / script_name
    (scripts / script_name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return {
        "workspaceName": "hook-run",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {hook_name: f"scripts/{script_name}"},
    }


@pytest.mark.smoke
def test_run_hook_ok(tmp_path):
    cfg = _cfg_with_hooks(tmp_path, "tables", "hook_ok.py")
    assert run_hook("tables", cfg) == 0


@pytest.mark.smoke
def test_run_hook_fail_propagates_exit_code(tmp_path):
    cfg = _cfg_with_hooks(tmp_path, "tables", "hook_fail.py")
    assert run_hook("tables", cfg) == 1


@pytest.mark.smoke
def test_run_hook_missing_script(tmp_path):
    cfg = {
        "workspaceName": "x",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "scripts/missing.py"},
    }
    assert run_hook("tables", cfg) == 1


@pytest.mark.smoke
def test_run_hook_unconfigured(tmp_path):
    cfg = {
        "workspaceName": "x",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
    }
    assert run_hook("tables", cfg) == 1
