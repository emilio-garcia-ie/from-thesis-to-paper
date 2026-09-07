"""Offline end-to-end scaffold and configured pipeline fixture."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "python")
    env.pop("FTTP_CONFIG", None)
    return subprocess.run(
        [sys.executable, "-m", "fttp", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.smoke
def test_scaffold_then_pipeline_with_real_offline_hooks(tmp_path):
    result = _run(tmp_path, "scaffold", "--slug", "integration-ws", "--parent", str(tmp_path))
    assert result.returncode == 0, result.stderr
    workspace = tmp_path / "integration-ws"
    config_path = workspace / "fttp.config.json"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    cfg["paper"]["venueProfiles"]["primary"]["build"] = None
    for name in ("tables", "evidence", "figures"):
        rel = f"scripts/{name}.py"
        cfg["hooks"][name] = rel
        path = workspace / rel
        path.write_text("from pathlib import Path\nPath('stage-" + name + "').touch()\n", encoding="utf-8")
    cfg["hooks"]["compile"] = "scripts/compile.py"
    (workspace / cfg["hooks"]["compile"]).write_text(
        "from pathlib import Path\nPath('paper/main.pdf').write_bytes(b'%PDF fixture')\n",
        encoding="utf-8",
    )
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    result = _run(workspace, "pipeline")
    assert result.returncode == 0, result.stderr
    assert (workspace / "paper/main.pdf").stat().st_size > 0
    assert all((workspace / f"stage-{name}").exists() for name in ("tables", "evidence", "figures"))
