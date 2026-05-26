"""Venue templatePath and empty paper/latex doctor checks."""

from __future__ import annotations

import pytest

from fttp.config import doctor_workspace_checks, validate_venue_profiles

from pathlib import Path


def _venue_cfg(root: Path, **paper_extra) -> dict:
    paper = {
        "dir": "paper",
        "mainTex": "main.tex",
        "activeVenue": "primary",
        "venueProfiles": {
            "primary": {
                "mainTex": "main.tex",
                "authorGuidelinesUrl": "https://example.com/guidelines",
                "templatePath": "paper/latex/vendor",
                "templateDeferred": False,
            }
        },
    }
    paper.update(paper_extra)
    return {
        "workspaceName": "t",
        "repoRoot": str(root),
        "paper": paper,
    }


@pytest.mark.smoke
def test_validate_venue_rejects_absolute_template_path(tmp_path):
    cfg = _venue_cfg(tmp_path)
    cfg["paper"]["venueProfiles"]["primary"]["templatePath"] = "/tmp/vendor"
    with pytest.raises(Exception, match="templatePath"):
        validate_venue_profiles(cfg)


@pytest.mark.smoke
def test_doctor_errors_missing_template_path_dir(tmp_path):
    cfg = _venue_cfg(tmp_path)
    errors, warnings = doctor_workspace_checks(cfg)
    assert any("templatePath not found" in e for e in errors)


@pytest.mark.smoke
def test_doctor_warns_empty_template_path_dir(tmp_path):
    vendor = tmp_path / "paper" / "latex" / "vendor"
    vendor.mkdir(parents=True)
    cfg = _venue_cfg(tmp_path)
    errors, warnings = doctor_workspace_checks(cfg)
    assert not errors
    assert any("templatePath is empty" in w for w in warnings)


@pytest.mark.smoke
def test_doctor_warns_empty_paper_latex_without_template_path(tmp_path):
    latex = tmp_path / "paper" / "latex"
    latex.mkdir(parents=True)
    cfg = _venue_cfg(tmp_path)
    del cfg["paper"]["venueProfiles"]["primary"]["templatePath"]
    errors, warnings = doctor_workspace_checks(cfg)
    assert any("primary venue" in e for e in errors)
    assert any("paper/latex/ is empty" in w for w in warnings)


@pytest.mark.smoke
def test_doctor_skips_empty_latex_when_template_deferred(tmp_path):
    latex = tmp_path / "paper" / "latex"
    latex.mkdir(parents=True)
    cfg = _venue_cfg(tmp_path)
    cfg["paper"]["venueProfiles"]["primary"]["templateDeferred"] = True
    del cfg["paper"]["venueProfiles"]["primary"]["templatePath"]
    errors, warnings = doctor_workspace_checks(cfg)
    assert not any("paper/latex/ is empty" in w for w in warnings)
    assert not any("templatePath is empty" in w for w in warnings)
