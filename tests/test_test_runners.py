"""Tests for the generated workspace test runner's truthful exit model."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_RUNNER = REPO / "templates" / "paper-workspace" / "scripts" / "run_tests.sh"


def _workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "runner-ws"
    shutil.copytree(REPO / "templates" / "paper-workspace", workspace)
    cfg = workspace / "fttp.config.json"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("{{WORKSPACE_SLUG}}", "runner-ws"), encoding="utf-8")
    return workspace


def _run(workspace: Path, mode: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["FTTP_FRAMEWORK_ROOT"] = str(REPO)
    env["FTTP_PYTHON"] = sys.executable
    return subprocess.run(
        [str(workspace / "scripts" / "run_tests.sh"), mode],
        cwd=workspace,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.smoke
def test_missing_tests_are_not_a_passing_smoke(tmp_path):
    result = _run(_workspace(tmp_path), "smoke")
    assert result.returncode != 0
    assert "no tests ran" in (result.stdout + result.stderr).lower() or "required test" in result.stderr.lower()


@pytest.mark.smoke
def test_failing_pytest_is_not_replaced_by_doctor(tmp_path):
    workspace = _workspace(tmp_path)
    tests = workspace / "tests"
    tests.mkdir()
    (tests / "test_fail.py").write_text(
        "import pytest\npytestmark = pytest.mark.smoke\n\ndef test_fail():\n    assert False\n",
        encoding="utf-8",
    )
    result = _run(workspace, "smoke")
    assert result.returncode != 0
    assert "assert false" in (result.stdout + result.stderr).lower()
    assert "doctor" not in (result.stdout + result.stderr).lower()


@pytest.mark.smoke
def test_passing_pytest_is_green(tmp_path):
    workspace = _workspace(tmp_path)
    tests = workspace / "tests"
    tests.mkdir()
    (tests / "test_ok.py").write_text(
        "import pytest\npytestmark = pytest.mark.smoke\n\ndef test_ok():\n    assert True\n",
        encoding="utf-8",
    )
    result = _run(workspace, "smoke")
    assert result.returncode == 0, result.stderr
