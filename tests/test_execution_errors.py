"""Expected subprocess launch failures stay concise and nonzero."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.commands import run_hook
from fttp.execution import run_local_command


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


@pytest.mark.smoke
def test_interrupt_returns_standard_exit_without_traceback(tmp_path, monkeypatch, capsys):
    class Interrupted:
        pid = 999999

        def wait(self, timeout=None):
            if timeout is None:
                raise KeyboardInterrupt
            return 0

        def kill(self):
            return None

    monkeypatch.setattr("fttp.execution.subprocess.Popen", lambda *args, **kwargs: Interrupted())
    monkeypatch.setattr("fttp.execution.os.killpg", lambda *args: None)
    assert run_local_command(["fixture"], cwd=tmp_path) == 130
    captured = capsys.readouterr().err
    assert "interrupted" in captured
    assert "Traceback" not in captured


@pytest.mark.smoke
def test_python_hook_uses_explicit_research_interpreter(tmp_path, monkeypatch):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    hook = scripts / "hook.py"
    hook.write_text("", encoding="utf-8")
    cfg = {
        "workspaceName": "exec-workspace",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "scripts/hook.py"},
    }
    seen: list[str] = []
    monkeypatch.setenv("FTTP_HOOK_PYTHON", "/opt/research/python")
    monkeypatch.setattr("fttp.commands.run_local_command", lambda command, **_: seen.extend(command) or 0)
    assert run_hook("tables", cfg) == 0
    assert seen[0] == "/opt/research/python"
