---
name: evidence-join-auditor
description: SA4 triangulation auditor — catalog vs log vs thesis table joins and discrepancy registry
---

# Evidence join auditor (SA4)

## Triggers

- After SA3 archaeology report exists.
- Before SA7 paper strategy signs `evidence_path`.
- User reports mismatch between thesis PDF table and exported JSON.

## Read order

1. `memory/evidence_archaeology_report.md`.
2. `memory/thesis_experiment_catalog.md` (catalog column definitions).
3. SA3b output if `optimization-or` pack ran (`math-audit` discrepancies separate file).
4. `memory/paper_strategy_brief.md` if draft exists (do not override signed fields).

## Steps

1. Define join keys: `experiment_id`, `model_id`, instance slug, run folder name.
2. For each critical cell (objective, gap, runtime): triangulate **thesis table | catalog | log tail | JSON solution**.
3. Register each mismatch in `memory/evidence_discrepancies.md` with recommended public value (`thesis_tables_only` vs `log_authoritative` — default per brief).
4. Mark rows **blocked** for Results prose until user picks policy for `DISCREPANCY` rows.
5. Produce join diagram or table: source A ↔ source B match rate.
6. Recommend `evidence_path` for SA7: `recompute_A` | `thesis_only_B` | `hybrid_B_plus`.

## Forbidden

- Hiding discrepancies to meet narrative arc.
- Choosing log values for published table cells when brief says `thesis_tables_only` without documenting in REPRODUCIBILITY only.
- Editing verification run folders to “fix” joins.

## Verify

- `memory/evidence_discrepancies.md` exists (may be empty if all OK).
- Join report states match rate for Cap.4 and Cap.5 anchor experiments.
- HANDOFF → SA7 (strategy); async SA5 may start after SA4 per launch map.
