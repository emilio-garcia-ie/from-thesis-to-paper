---
name: evidence-archaeologist
description: SA3 evidence archaeologist — twin notebooks, Excel summaries, catalog rows, no log dumps
---

# Evidence archaeologist (SA3)

## Triggers

- Parallel or sequential gate after SA2b; before SA4 join audit.
- User asks to “find thesis numbers”, “archaeology”, “which log matches T###”.
- Building or refreshing `memory/thesis_experiment_catalog.md`.

## Read order

1. `memory/workspace_intake.md` read-only roots.
2. `memory/thesis_experiment_run_artifacts.md` or template (artifact glossary).
3. Excel/CSV summaries under verification trees (**search, do not cat huge logs**).
4. Master notebooks in `Thesis Code/` (read-only).

## Steps

1. **Locate twin notebooks** vs master templates; note which contain execution loops.
2. For each thesis table row needed by the brief: find **catalog id**, export path, or summary spreadsheet cell.
3. Record tier: **A** recompute path, **B** thesis/catalog only, **C** missing → `TBD`.
4. Update catalog memory with source path column (relative to read-only root).
5. Write `memory/evidence_archaeology_report.md` with coverage % and top gaps.
6. Never paste multi-MB log bodies into chat — tail ≤50 lines or scripted extract only.

## Forbidden

- Writing to OneDrive verification trees or master notebooks.
- Inventing objectives because a log “looks close”.
- Loading `optimization-or` pack unless config enables it (math audit is SA3b).

## Verify

- Report lists every table id the paper strategy will need, each `OK` | `TBD` | `DISCREPANCY`.
- Token-safe: no full log file reads into model context.
- HANDOFF → SA4 (join auditor); SA3b optional in parallel if pack enabled.
