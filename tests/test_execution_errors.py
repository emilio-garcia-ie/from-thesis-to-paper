"""Expected subprocess launch failures stay concise and nonzero."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.commands import run_hook


@pytest.mark.smoke
def test_missing_executable_has_integer_failure_without_traceback(tmp_path, capsys):
    cfg = {
        "workspaceName": "exec-workspace",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "scripts/no-such-hook"},
    }
    (tmp_path / "scripts").mkdir()
    assert run_hook("tables", cfg) == 1
    assert "Traceback" not in capsys.readouterr().err


@pytest.mark.smoke
def test_nonexecutable_hook_is_reported(tmp_path, capsys):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    hook = scripts / "hook.sh"
    hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    hook.chmod(0o644)
    cfg = {
        "workspaceName": "exec-workspace",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "scripts/hook.sh"},
    }
    assert run_hook("tables", cfg) == 1
    assert "Traceback" not in capsys.readouterr().err
