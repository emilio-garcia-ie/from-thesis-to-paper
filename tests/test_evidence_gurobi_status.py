"""Gurobi status map tests."""

from __future__ import annotations

import pytest

from fttp.evidence.gurobi_status import termination_from_gurobi_status
from fttp.evidence.merge_fallback import candidate_from_status_code, row_eligible_for_fallback


@pytest.mark.smoke
def test_termination_from_gurobi_status():
    assert termination_from_gurobi_status(2) == "OPTIMAL"
    assert termination_from_gurobi_status(3) == "INFEASIBLE"
    assert termination_from_gurobi_status(9) == "TIME_LIMIT"
    assert termination_from_gurobi_status(99).startswith("STATUS_")


@pytest.mark.smoke
def test_candidate_from_status_code_infeasible_clears_objective():
    term, obj = candidate_from_status_code(3, objective=1.0)  # type: ignore[misc]
    assert term == "INFEASIBLE"
    assert obj is None


@pytest.mark.smoke
def test_row_eligible_for_fallback():
    assert row_eligible_for_fallback({"termination": "UNKNOWN", "objective_log": ""})
    assert not row_eligible_for_fallback(
        {"termination": "OPTIMAL", "objective_log": "1.0"}
    )
