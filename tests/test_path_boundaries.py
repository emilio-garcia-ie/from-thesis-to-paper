"""Configuration and execution confinement regression tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fttp.commands import run_hook
from fttp.config import FttpConfigError, load_config


def _write_config(root: Path, **updates) -> Path:
    cfg = {
        "workspaceName": "safe-workspace",
        "repoRoot": str(root),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
    }
    cfg.update(updates)
    path = root / "fttp.config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


@pytest.mark.smoke
@pytest.mark.parametrize("field,value", [("workspaceName", 1), ("repoRoot", 1)])
def test_invalid_scalar_types_fail_before_use(tmp_path, field, value):
    path = _write_config(tmp_path, **{field: value})
    with pytest.raises(FttpConfigError):
        load_config(path)


@pytest.mark.smoke
def test_active_venue_requires_declared_profile(tmp_path):
    path = _write_config(
        tmp_path,
        paper={"dir": "paper", "mainTex": "main.tex", "activeVenue": "primary"},
    )
    with pytest.raises(FttpConfigError, match="activeVenue"):
        load_config(path)


@pytest.mark.smoke
def test_read_only_root_overlap_is_rejected_in_both_directions(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    path = _write_config(tmp_path, readOnlyRoots=[str(child)])
    with pytest.raises(FttpConfigError, match="overlaps"):
        load_config(path)

    parent = tmp_path.parent
    path = _write_config(tmp_path, readOnlyRoots=[str(parent)])
    with pytest.raises(FttpConfigError, match="overlaps"):
        load_config(path)


@pytest.mark.smoke
def test_symlink_escape_is_rejected(tmp_path):
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    paper_link = tmp_path / "paper"
    paper_link.symlink_to(outside, target_is_directory=True)
    path = _write_config(tmp_path)
    with pytest.raises(FttpConfigError, match="outside"):
        load_config(path)


@pytest.mark.smoke
def test_rejected_hook_does_not_execute_external_marker(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = outside / "marker"
    script = outside / "hook.py"
    script.write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n", encoding="utf-8")
    cfg = {
        "workspaceName": "safe-workspace",
        "repoRoot": str(tmp_path),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
        "hooks": {"tables": "../outside/hook.py"},
    }
    with pytest.raises(FttpConfigError):
        load_config(_write_config(tmp_path, **{ "hooks": cfg["hooks"] }))
    assert not marker.exists()
