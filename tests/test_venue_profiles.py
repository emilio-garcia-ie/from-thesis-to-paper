"""Venue profile resolution tests."""

from __future__ import annotations

import pytest

from fttp.config import active_venue_profile, resolve_active_main_tex

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_resolve_active_main_tex_default():
    cfg = {
        "repoRoot": str(REPO),
        "paper": {"dir": "templates/paper", "mainTex": "README.md"},
    }
    path = resolve_active_main_tex(cfg)
    assert path.name == "README.md"
    assert "templates" in str(path)


@pytest.mark.smoke
def test_resolve_active_main_tex_venue_override(tmp_path):
    paper = tmp_path / "paper"
    paper.mkdir()
    (paper / "main.tex").write_text("% default", encoding="utf-8")
    (paper / "venue.tex").write_text("% venue", encoding="utf-8")
    cfg = {
        "repoRoot": str(tmp_path),
        "paper": {
            "dir": "paper",
            "mainTex": "main.tex",
            "activeVenue": "alt",
            "venueProfiles": {
                "alt": {"mainTex": "venue.tex"},
            },
        },
    }
    assert resolve_active_main_tex(cfg).name == "venue.tex"
    assert active_venue_profile(cfg)["mainTex"] == "venue.tex"
