"""Offline tests for the optional Overleaf launcher boundary."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LAUNCHER = REPO / "templates" / "scripts" / "overleaf_mcp.sh.example"


@pytest.mark.smoke
def test_launcher_sources_workspace_env_only(tmp_path):
    workspace = tmp_path / "paper workspace"
    scripts = workspace / "scripts"
    scripts.mkdir(parents=True)
    launcher = scripts / "overleaf_mcp.sh"
    launcher.write_text(LAUNCHER.read_text(encoding="utf-8"), encoding="utf-8")
    launcher.chmod(0o755)
    (workspace / ".env").write_text("FTTP_TEST_MARKER=workspace\n", encoding="utf-8")
    (tmp_path / ".env").write_text("FTTP_TEST_MARKER=parent\n", encoding="utf-8")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_npx = fake_bin / "npx"
    fake_npx.write_text(
        "#!/usr/bin/env bash\n"
        "printf 'cwd=%s marker=%s args=%s\\n' \"$PWD\" \"${FTTP_TEST_MARKER:-missing}\" \"$*\"\n",
        encoding="utf-8",
    )
    fake_npx.chmod(0o755)

    env = dict(os.environ)
    env["PATH"] = f"{fake_bin}{os.pathsep}{env.get('PATH', '')}"
    unrelated = tmp_path / "unrelated"
    unrelated.mkdir()
    result = subprocess.run(
        [str(launcher), "--flag", "with spaces"],
        cwd=unrelated,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert f"cwd={workspace}" in result.stdout
    assert "marker=workspace" in result.stdout
    assert "marker=parent" not in result.stdout
    assert "--flag with spaces" in result.stdout
