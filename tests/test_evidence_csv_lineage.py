"""Lineage CSV validation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from fttp.evidence.csv_lineage import validate_lineage_csv

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL = FIXTURES / "lineage_minimal.csv"


@pytest.mark.smoke
def test_validate_lineage_minimal_fixture():
    assert validate_lineage_csv(MINIMAL) == []


@pytest.mark.smoke
def test_validate_lineage_missing_column(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("id,termination\nT001,OPTIMAL\n", encoding="utf-8")
    errors = validate_lineage_csv(bad)
    assert any("missing columns" in e for e in errors)


@pytest.mark.smoke
def test_validate_lineage_duplicate_id(tmp_path):
    dup = tmp_path / "dup.csv"
    dup.write_text(
        "id,termination,objective_log,lineage_status\n"
        "T001,OPTIMAL,1,CONFIRMED\n"
        "T001,OPTIMAL,2,CONFIRMED\n",
        encoding="utf-8",
    )
    errors = validate_lineage_csv(dup)
    assert any("duplicate" in e for e in errors)
