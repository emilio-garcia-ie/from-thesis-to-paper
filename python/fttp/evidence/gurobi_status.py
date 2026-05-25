"""Gurobi SolutionInfo.Status → lineage termination labels (generic)."""

from __future__ import annotations

# Gurobi Status codes (SolutionInfo.Status) — reference manual subset.
GUROBI_STATUS: dict[int, str] = {
    1: "LOADED",
    2: "OPTIMAL",
    3: "INFEASIBLE",
    4: "INF_OR_UNBD",
    5: "UNBOUNDED",
    6: "CUTOFF",
    7: "ITERATION_LIMIT",
    8: "NODE_LIMIT",
    9: "TIME_LIMIT",
    10: "SOLUTION_LIMIT",
    11: "INTERRUPTED",
    12: "NUMERIC",
    13: "SUBOPTIMAL",
    14: "INPROGRESS",
    15: "USER_OBJ_LIMIT",
}

JSON_STATUS_ALLOW = frozenset({2, 3, 9})


def termination_from_gurobi_status(code: int | None) -> str:
    if code is None:
        return "UNKNOWN"
    label = GUROBI_STATUS.get(code, f"STATUS_{code}")
    if label == "OPTIMAL":
        return "OPTIMAL"
    if label == "INFEASIBLE":
        return "INFEASIBLE"
    if label == "TIME_LIMIT":
        return "TIME_LIMIT"
    return label
