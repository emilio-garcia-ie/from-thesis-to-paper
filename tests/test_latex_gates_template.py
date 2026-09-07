"""Deterministic LaTeX gate checks for the shipped workspace fixture."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DEFAULT_MAIN = REPO / "templates" / "paper-workspace" / "paper" / "main.tex"


def _main_tex_path() -> Path:
    env = os.environ.get("FTTP_MAIN_TEX", "").strip()
    if env:
        path = Path(env).expanduser()
        if not path.is_file():
            raise AssertionError(f"FTTP_MAIN_TEX does not exist: {path}")
        return path
    assert DEFAULT_MAIN.is_file(), f"shipped LaTeX fixture is missing: {DEFAULT_MAIN}"
    return DEFAULT_MAIN


@pytest.fixture
def main_text() -> str:
    path = _main_tex_path()
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
