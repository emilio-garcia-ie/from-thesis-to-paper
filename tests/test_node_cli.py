"""Parity and transport tests for the optional Node launcher."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
NODE = REPO / "packages" / "cli" / "src" / "cli.js"


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "python")
    env["FTTP_PYTHON"] = sys.executable
    env.pop("FTTP_CONFIG", None)
    return env


def _run_python(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "fttp", *args],
        cwd=cwd,
        env=_env(),
        text=True,
        capture_output=True,
        check=False,
    )


def _run_node(cwd: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(NODE), *args],
        cwd=cwd,
        env=env or _env(),
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.smoke
def test_help_and_invalid_arguments_match_python(tmp_path):
    for args in (("--help",), ("doctor", "--bad-option")):
        py = _run_python(tmp_path, *args)
        node = _run_node(tmp_path, *args)
        assert node.returncode == py.returncode
        assert node.stdout == py.stdout
        assert node.stderr == py.stderr


@pytest.mark.smoke
def test_wrapper_streams_large_hook_output_and_preserves_config(tmp_path):
    script = tmp_path / "hook.py"
    script.write_text("print('x' * 2_000_000)\n", encoding="utf-8")
    config = {
        "workspaceName": "node-ws",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "hook.py"},
    }
    (tmp_path / "fttp.config.json").write_text(json.dumps(config), encoding="utf-8")
    py = _run_python(tmp_path, "tables")
    node = _run_node(tmp_path, "tables")
    assert py.returncode == node.returncode == 0
    assert len(node.stdout) >= 2_000_000
    assert node.stdout == py.stdout
    assert node.stderr == py.stderr


@pytest.mark.smoke
def test_wrapper_reports_missing_interpreter_without_traceback(tmp_path):
    env = _env()
    env["FTTP_PYTHON"] = str(tmp_path / "missing-python")
    result = _run_node(tmp_path, "doctor", env=env)
    assert result.returncode == 1
    assert "cannot start" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.smoke
def test_wrapper_version_is_local_and_does_not_need_python(tmp_path):
    env = _env()
    env["FTTP_PYTHON"] = str(tmp_path / "missing-python")
    result = _run_node(tmp_path, "--version", env=env)
    assert result.returncode == 0
    assert result.stdout.strip() == "from-thesis-to-paper 0.2.0"
