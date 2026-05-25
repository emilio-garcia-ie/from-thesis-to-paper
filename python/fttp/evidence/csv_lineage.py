"""Validate lineage CSV columns (generic minimum schema)."""

from __future__ import annotations

import csv
from pathlib import Path

MINIMAL_REQUIRED_COLUMNS = (
    "id",
    "termination",
    "objective_log",
    "lineage_status",
)

ALLOWED_LINEAGE_STATUS = frozenset(
    {"", "CONFIRMED", "DISCREPANCY", "TBD", "UNKNOWN"}
)

ALLOWED_TERMINATION = frozenset(
    {
        "",
        "UNKNOWN",
        "OPTIMAL",
        "INFEASIBLE",
        "TIME_LIMIT",
        "LOADED",
        "UNBOUNDED",
        "SUBOPTIMAL",
    }
)


def load_lineage_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_lineage_csv(
    path: Path,
    *,
    required_columns: tuple[str, ...] = MINIMAL_REQUIRED_COLUMNS,
    min_rows: int = 1,
) -> list[str]:
    """Return a list of validation error messages (empty if OK)."""
    errors: list[str] = []

    if not path.is_file():
        return [f"file not found: {path}"]

    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                return ["CSV has no header row"]
            fieldnames = list(reader.fieldnames)
            missing_cols = [c for c in required_columns if c not in fieldnames]
            if missing_cols:
                errors.append(f"missing columns: {', '.join(missing_cols)}")
                return errors

            rows = list(reader)
    except OSError as exc:
        return [f"cannot read CSV: {exc}"]

    if len(rows) < min_rows:
        errors.append(f"expected at least {min_rows} row(s), got {len(rows)}")

    seen_ids: set[str] = set()
    for idx, row in enumerate(rows, start=2):
        eid = (row.get("id") or "").strip()
        if not eid:
            errors.append(f"row {idx}: empty id")
            continue
        if eid in seen_ids:
            errors.append(f"row {idx}: duplicate id '{eid}'")
        seen_ids.add(eid)

        term = (row.get("termination") or "").strip().upper()
        if term and term not in ALLOWED_TERMINATION and not term.startswith("STATUS_"):
            errors.append(f"row {idx} ({eid}): unusual termination '{term}'")

        status = (row.get("lineage_status") or "").strip().upper()
        if status and status not in ALLOWED_LINEAGE_STATUS:
            errors.append(f"row {idx} ({eid}): invalid lineage_status '{status}'")

    return errors
