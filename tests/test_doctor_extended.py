"""Extended doctor_workspace_checks (onboarding v2)."""

from __future__ import annotations

import pytest

from fttp.config import doctor_workspace_checks


def _minimal_cfg(root, **extra):
    cfg = {
        "workspaceName": "test",
        "repoRoot": str(root),
        "paper": {"dir": "paper", "mainTex": "main.tex"},
    }
    cfg.update(extra)
    return cfg


@pytest.mark.smoke
def test_doctor_warns_slug_dirname_mismatch(tmp_path):
    slug_dir = tmp_path / "my-slug"
    slug_dir.mkdir()
    cfg = _minimal_cfg(slug_dir, workspaceSlug="other-slug")
    errors, warnings = doctor_workspace_checks(cfg)
    assert not errors
    assert any("workspaceSlug" in w and "repoRoot" in w for w in warnings)


@pytest.mark.smoke
def test_doctor_errors_read_only_root_inside_repo(tmp_path):
    ro = tmp_path / "internal" / "thesis"
    ro.mkdir(parents=True)
    cfg = _minimal_cfg(tmp_path, readOnlyRoots=[str(ro)])
    errors, warnings = doctor_workspace_checks(cfg)
    assert any("readOnlyRoots" in e and "repoRoot" in e for e in errors)
    assert not warnings


@pytest.mark.smoke
def test_doctor_no_slug_warning_when_names_match(tmp_path):
    cfg = _minimal_cfg(tmp_path, workspaceSlug=tmp_path.name)
    errors, warnings = doctor_workspace_checks(cfg)
    assert not any("workspaceSlug" in w for w in warnings)
    assert not errors
