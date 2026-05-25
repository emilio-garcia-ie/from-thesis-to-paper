"""JSON/status fallback helpers (generic; no workspace path discovery)."""

from __future__ import annotations

from fttp.evidence.gurobi_status import JSON_STATUS_ALLOW, termination_from_gurobi_status

TERM_UNKNOWN = frozenset({"", "UNKNOWN"})


def row_eligible_for_fallback(row: dict[str, str]) -> bool:
    """True when termination or objective_log is empty/unknown (merge candidate)."""
    term = (row.get("termination") or "").strip().upper()
    obj = (row.get("objective_log") or "").strip()
    return term in TERM_UNKNOWN or not obj


def candidate_from_status_code(
    code: int | None,
    *,
    objective: float | None = None,
) -> tuple[str, float | None] | None:
    """Map Gurobi status code to (termination, objective) for fallback merge."""
    if code not in JSON_STATUS_ALLOW:
        return None
    term = termination_from_gurobi_status(code)
    if not term or term == "UNKNOWN":
        return None
    obj = objective
    if term == "INFEASIBLE":
        obj = None
    return term, obj
