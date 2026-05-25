"""Generic evidence helpers (Gurobi status map, lineage CSV validation)."""

from fttp.evidence.csv_lineage import (
    MINIMAL_REQUIRED_COLUMNS,
    load_lineage_rows,
    validate_lineage_csv,
)
from fttp.evidence.gurobi_status import (
    GUROBI_STATUS,
    JSON_STATUS_ALLOW,
    termination_from_gurobi_status,
)
from fttp.evidence.merge_fallback import (
    candidate_from_status_code,
    row_eligible_for_fallback,
)

__all__ = [
    "GUROBI_STATUS",
    "JSON_STATUS_ALLOW",
    "MINIMAL_REQUIRED_COLUMNS",
    "candidate_from_status_code",
    "load_lineage_rows",
    "row_eligible_for_fallback",
    "termination_from_gurobi_status",
    "validate_lineage_csv",
]
