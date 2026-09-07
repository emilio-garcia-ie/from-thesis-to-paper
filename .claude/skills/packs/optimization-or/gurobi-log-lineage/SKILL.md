---
name: gurobi-log-lineage
description: Batch Gurobi log parsing, lineage CSV updates, token-safe evidence joins
---

# Gurobi log lineage

## Triggers

- Regenerating or validating `experimentos/evidence/log_lineage.csv`.
- User asks to parse `registro_*.txt` or `*.log` without pasting logs into chat.
- SA4 join audit needs `objective_log`, `gap_log`, `runtime_log_sec` from solver transcripts.

## Read order

1. `memory/thesis_experiment_run_artifacts.md` — log glossary and forbidden full-file reads.
2. `experimentos/evidence/log_lineage.csv` (writable) and `scripts/archaeology/parse_logs_gurobi_logtools.py`.
3. `scripts/archaeology/build_log_lineage.py` for path discovery rules.
4. Catalog / `memory/thesis_experiment_catalog.md` for `reported_*` vs log columns.

## Steps

1. **Never** load multi-MB logs into model context — use batch Python only.
2. **Hooks first:** `python -m fttp lineage build` (runs `hooks.lineageBuild` under `repoRoot` from `fttp.config.json`).
3. When paths or catalog rows changed, run the consumer script directly if needed: `python scripts/archaeology/build_log_lineage.py`.
4. **Validate (framework):** `python -m fttp lineage validate --csv experimentos/evidence/log_lineage.csv` — generic column checks via `fttp.evidence` (no OneDrive paths in OSS).
5. Batch parse: `python scripts/archaeology/parse_logs_gurobi_logtools.py` (gurobi-logtools or tail fallback).
6. **OneDrive-safe:** prefer staged `experimentos/evidence/log_cache/` copies; use `tail -n 250` subprocess, not full read.
7. Map fields: `objective_log`, `gap_log`, `runtime_log_sec`, `termination` → lineage columns Block C/F.
8. **Join:** compare to `reported_objective` with catalog tolerance; set `lineage_status` `CONFIRMED` | `DISCREPANCY` | `TBD`.
9. Respect `golden_locked=Y` rows — do not overwrite without explicit user approval and hash check.
10. Summarize in `memory/evidence_join_report.md` (core SA4) with counts, not raw log lines.
11. Figures optional: `experimentos/evidence/figures/lineage_*.png` via existing scripts.

## Forbidden

- Pasting `registro_*.txt` or full `.log` into chat.
- Editing logs under read-only verification roots.
- Picking the favorable objective when log and catalog disagree.
- Adding GurobiMCP or per-file agent `Read` on logs.

## Verify

- `python -m fttp lineage validate` PASS on `evidence.lineageCsv` (or `--csv` path).
- CSV parses: `python -c "import csv; list(csv.DictReader(open('experimentos/evidence/log_lineage.csv')))"`
- Row count stable vs catalog scope documented in join report.
- At least one `CONFIRMED` golden row (e.g. T185) unchanged unless repro approved.
- `./scripts/run_tests.sh smoke` PASS if scripts touched.
- HANDOFF → SA4 evidence-join-auditor (core); SA8 must not cite log-only numbers without join status.
