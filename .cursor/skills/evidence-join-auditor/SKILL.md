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
3. Register each mismatch in `memory/evidence_discrepancies.md` and/or `memory/discrepancy_registry.md` with recommended public value (`thesis_tables_only` vs `log_authoritative` — default per brief).
4. Mark rows **blocked** for Results prose until user picks policy for `DISCREPANCY` rows; leave **`TBD`** visible where no authoritative source exists.
5. Produce join diagram or table: source A ↔ source B match rate; write `memory/join_audit_report.md` when useful.
6. Recommend `evidence_path` for SA7: `recompute_A` | `thesis_only_B` | `hybrid_B_plus`.
7. Run **G4-evidence** AUDIT / APPROVE when `workflowProfile` requires G4 (below) **before** HANDOFF to SA7.

## G4-evidence — AUDIT / APPROVE (profile-dependent)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md).

| `workflowProfile` | G4 required? |
|-------------------|--------------|
| `paper_only` | No — note G4 waived in log if row exists |
| `paper_audit`, `paper_audit_repro`, `full_pipeline` | **Yes** — blocks SA7 and SA8 |

After catalog, discrepancy registry, and join report are updated:

```text
AUDIT: G4-evidence — review memory/thesis_experiment_catalog.md, memory/discrepancy_registry.md (and evidence_discrepancies), experimentos/evidence/* if present, join_audit_report
Checklist:
- Every material TBD and DISCREPANCY visible (not buried)
- User agrees numeric authority (catalog vs log vs thesis table) per row or policy
- No silent picks favoring narrative
APPROVE_ASK: Confirm evidence join reflects your runs and thesis tables. Reply APPROVED: G4-evidence (EN) or APROBADO: G4-evidence (ES) or corrections.
```

On user approval: update row **`G4-evidence`** in `memory/user_approval_log.md`.

**When G4 is required but not approved:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA7, SA8 — missing approved row for G4-evidence
```

## Forbidden

- Hiding discrepancies to meet narrative arc.
- Choosing log values for published table cells when brief says `thesis_tables_only` without documenting in REPRODUCIBILITY only.
- Editing verification run folders to “fix” joins.

## Verify

- `memory/evidence_discrepancies.md` / `memory/discrepancy_registry.md` exists (may be empty if all OK).
- Join report states match rate for Cap.4 and Cap.5 anchor experiments.
- When profile requires G4: `memory/user_approval_log.md` has **G4-evidence** `approved` before HANDOFF → SA7.
- HANDOFF → SA7 (strategy) only after G4 approved or G4 waived for `paper_only`; async SA5 may start after SA4 per launch map.
