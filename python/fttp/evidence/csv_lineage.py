"""Validate lineage CSV columns (generic minimum schema)."""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path

from fttp.evidence.gurobi_status import GUROBI_STATUS

MINIMAL_REQUIRED_COLUMNS = (
    "id",
    "termination",
    "objective_log",
    "lineage_status",
)

ALLOWED_LINEAGE_STATUS = frozenset(
    {"", "CONFIRMED", "DISCREPANCY", "TBD", "UNKNOWN"}
)

ALLOWED_TERMINATION = frozenset({"", "UNKNOWN", *GUROBI_STATUS.values()})
_STATUS_LABEL = re.compile(r"^STATUS_-?\d+$")


def load_lineage_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle, strict=True))
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise ValueError(f"cannot parse lineage CSV {path}: {exc}") from exc


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
        handle = path.open(encoding="utf-8", newline="")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read CSV: {exc}"]

    row_count = 0
    try:
        with handle:
            reader = csv.DictReader(handle, strict=True)
            if reader.fieldnames is None:
                return ["CSV has no header row"]
            fieldnames = list(reader.fieldnames)
            if any(name is None or not str(name).strip() for name in fieldnames):
                errors.append("CSV header contains an empty column name")
            duplicate_headers = sorted(
                {name for name in fieldnames if name is not None and fieldnames.count(name) > 1}
            )
            if duplicate_headers:
                errors.append(f"duplicate header(s): {', '.join(duplicate_headers)}")
            missing_cols = [c for c in required_columns if c not in fieldnames]
            if missing_cols:
                errors.append(f"missing columns: {', '.join(missing_cols)}")
                return errors

            seen_ids: set[str] = set()
            for idx, row in enumerate(reader, start=2):
                row_count += 1
                if None in row:
                    errors.append(f"row {idx}: too many fields")
                if any(value is None for value in row.values()):
                    errors.append(f"row {idx}: missing field")
                eid = (row.get("id") or "").strip()
                if not eid:
                    errors.append(f"row {idx}: empty id")
                    continue
                if eid in seen_ids:
                    errors.append(f"row {idx}: duplicate id '{eid}'")
                seen_ids.add(eid)

                term = (row.get("termination") or "").strip().upper()
                if term and term not in ALLOWED_TERMINATION and not _STATUS_LABEL.fullmatch(term):
                    errors.append(f"row {idx} ({eid}): unusual termination '{term}'")

                status = (row.get("lineage_status") or "").strip().upper()
                if status and status not in ALLOWED_LINEAGE_STATUS:
                    errors.append(f"row {idx} ({eid}): invalid lineage_status '{status}'")

                objective = (row.get("objective_log") or "").strip()
                if objective:
                    try:
                        value = float(objective)
                    except ValueError:
                        errors.append(f"row {idx} ({eid}): objective_log is not numeric")
                    else:
                        if not math.isfinite(value):
                            errors.append(f"row {idx} ({eid}): objective_log must be finite")
                        if term == "INFEASIBLE":
                            errors.append(f"row {idx} ({eid}): INFEASIBLE rows cannot have objective_log")
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"cannot parse CSV: {exc}")

    if row_count < min_rows:
        errors.append(f"expected at least {min_rows} row(s), got {row_count}")

    return errors
