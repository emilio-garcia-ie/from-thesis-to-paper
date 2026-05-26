"""Tests for fttp venue validate subcommand."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.venue_validate import cmd_venue_validate, validate_venue


def _minimal_cfg(root: Path) -> dict:
    return {
        "workspaceName": "v",
        "repoRoot": str(root),
        "paper": {
            "dir": "paper",
            "mainTex": "main.tex",
            "activeVenue": "primary",
            "venueProfiles": {
                "primary": {
                    "mainTex": "main.tex",
                    "authorGuidelinesUrl": "https://example.com/g",
                    "templateDeferred": True,
                }
            },
        },
    }


@pytest.mark.smoke
def test_venue_validate_ok_with_deferred_template(tmp_path):
    paper = tmp_path / "paper"
    paper.mkdir()
    (paper / "main.tex").write_text(
        r"\documentclass{article}" + "\n\\begin{document}\n\\end{document}\n",
        encoding="utf-8",
    )
    cfg = _minimal_cfg(tmp_path)
    errors, warnings = validate_venue(cfg)
    assert not errors
    assert cmd_venue_validate(cfg) == 0


@pytest.mark.smoke
def test_venue_validate_warns_missing_documentclass_cls(tmp_path):
    paper = tmp_path / "paper"
    latex = paper / "latex"
    latex.mkdir(parents=True)
    (paper / "main.tex").write_text(
        r"\documentclass{elsarticle}" + "\n",
        encoding="utf-8",
    )
    cfg = _minimal_cfg(tmp_path)
    cfg["paper"]["venueProfiles"]["primary"]["templateDeferred"] = False
    cfg["paper"]["venueProfiles"]["primary"]["templatePath"] = "paper/latex"
    errors, warnings = validate_venue(cfg)
    assert not errors
    assert any("elsarticle" in w for w in warnings)
