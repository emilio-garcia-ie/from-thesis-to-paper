"""Pipeline output and stage-order regressions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp.commands import cmd_compile
from fttp.pipeline import run_pipeline


def _config(root: Path, hooks: dict[str, str]) -> dict:
    paper = root / "paper"
    paper.mkdir(exist_ok=True)
    (paper / "main.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    return {
        "workspaceName": "pipeline-ws",
        "repoRoot": str(root),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": hooks,
    }


def _hook(root: Path, rel: str, body: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


@pytest.mark.smoke
def test_pipeline_stops_on_placeholder_before_later_hooks(tmp_path, capsys):
    hooks = {
        "tables": "scripts/tables.py",
        "evidence": "scripts/evidence.py",
        "figures": "scripts/figures.py",
        "compile": "scripts/compile.py",
    }
    for key, rel in hooks.items():
        _hook(tmp_path, rel, "import sys\nprint('placeholder', file=sys.stderr)\nsys.exit(1)\n")
    markers = tmp_path / "markers"
    markers.mkdir()
    # The first hook is the only one allowed to run in this failure case.
    _hook(tmp_path, hooks["tables"], f"from pathlib import Path\nPath({str(markers / 'tables')!r}).touch()\nimport sys\nsys.exit(1)\n")
    assert run_pipeline(_config(tmp_path, hooks)) == 1
    assert (markers / "tables").exists()
    assert not (markers / "evidence").exists()
    assert "stopped at 'tables'" in capsys.readouterr().err


@pytest.mark.smoke
def test_pipeline_requires_actual_compile_hook(tmp_path):
    cfg = _config(tmp_path, {})
    assert run_pipeline(cfg) == 1


@pytest.mark.smoke
def test_compile_requires_nonempty_pdf_after_successful_hook(tmp_path):
    hook = "scripts/compile.py"
    _hook(tmp_path, hook, "from pathlib import Path\nPath('paper/main.pdf').write_bytes(b'')\n")
    cfg = _config(tmp_path, {"compile": hook})
    assert cmd_compile(cfg) == 1
    _hook(tmp_path, hook, "from pathlib import Path\nPath('paper/main.pdf').write_bytes(b'%PDF fixture')\n")
    assert cmd_compile(cfg) == 0


@pytest.mark.smoke
def test_standalone_compile_existence_check_is_explicit(tmp_path, capsys):
    cfg = _config(tmp_path, {})
    (tmp_path / "paper" / "main.pdf").write_bytes(b"%PDF fixture")
    assert cmd_compile(cfg) == 0
    assert "existence check" in capsys.readouterr().out


@pytest.mark.smoke
def test_compile_rejects_pdf_symlink_escape(tmp_path):
    cfg = _config(tmp_path, {})
    outside = tmp_path.parent / f"{tmp_path.name}-pdf-outside"
    outside.write_bytes(b"%PDF fixture")
    (tmp_path / "paper" / "main.pdf").symlink_to(outside)
    assert cmd_compile(cfg) == 1
