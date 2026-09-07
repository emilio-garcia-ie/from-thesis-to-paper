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


@pytest.mark.smoke
@pytest.mark.parametrize("termination", ["INF_OR_UNBD", "WORK_LIMIT", "MEM_LIMIT", "STATUS_99", "UNKNOWN", ""])
def test_validator_accepts_status_labels_emitted_by_status_helper(tmp_path, termination):
    path = tmp_path / "status.csv"
    objective = "" if termination == "INFEASIBLE" else "1.25"
    path.write_text(
        "id,termination,objective_log,lineage_status\n"
        f"T001,{termination},{objective},UNKNOWN\n",
        encoding="utf-8",
    )
    errors = validate_lineage_csv(path)
    assert not any("unusual termination" in error for error in errors), errors


@pytest.mark.smoke
def test_validator_rejects_extra_fields_nonfinite_and_infeasible_objective(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "id,termination,objective_log,lineage_status\n"
        "T001,INFEASIBLE,2,CONFIRMED,extra\n"
        "T002,OPTIMAL,NaN,CONFIRMED\n",
        encoding="utf-8",
    )
    errors = validate_lineage_csv(path)
    assert any("too many fields" in error for error in errors)
    assert any("cannot have objective_log" in error for error in errors)
    assert any("finite" in error for error in errors)


@pytest.mark.smoke
def test_validator_reports_empty_and_malformed_input(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    assert any("no header" in error for error in validate_lineage_csv(empty))

    malformed = tmp_path / "malformed.csv"
    malformed.write_text(
        "id,termination,objective_log,lineage_status\nT001,\"OPTIMAL,1,CONFIRMED\n",
        encoding="utf-8",
    )
    assert any("parse" in error for error in validate_lineage_csv(malformed))

    empty_header = tmp_path / "empty-header.csv"
    empty_header.write_text(
        "id,,objective_log,lineage_status\nT001,OPTIMAL,1,CONFIRMED\n",
        encoding="utf-8",
    )
    assert any("empty column" in error for error in validate_lineage_csv(empty_header))
