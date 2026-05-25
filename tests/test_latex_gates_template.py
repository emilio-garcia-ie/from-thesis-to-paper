"""Parametrized LaTeX gate checks (optional FTTP_MAIN_TEX)."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DEFAULT_MAIN = REPO / "templates" / "paper" / "README.md"


def _main_tex_path() -> Path | None:
    env = os.environ.get("FTTP_MAIN_TEX", "").strip()
    if env:
        path = Path(env).expanduser()
        return path if path.is_file() else None
    if DEFAULT_MAIN.is_file():
        return DEFAULT_MAIN
    return None


@pytest.fixture
def main_text() -> str:
    path = _main_tex_path()
    if path is None:
        pytest.skip("Set FTTP_MAIN_TEX to a manuscript .tex file for gate tests")
    return path.read_text(encoding="utf-8")


@pytest.mark.smoke
def test_no_codepath_macro(main_text: str):
    hits = [ln for ln in main_text.splitlines() if r"\codepath{" in ln]
    assert hits == []


@pytest.mark.smoke
def test_no_thesis_self_cite_key(main_text: str):
    assert "ergc2025thesis" not in main_text


@pytest.mark.smoke
def test_no_lineage_discrepancy_macro_in_body(main_text: str):
    assert "lineageDiscrepancy" not in main_text


@pytest.mark.smoke
def test_paragraph_mini_headings_limited(main_text: str):
    assert len(re.findall(r"\\paragraph\{", main_text)) <= 8
