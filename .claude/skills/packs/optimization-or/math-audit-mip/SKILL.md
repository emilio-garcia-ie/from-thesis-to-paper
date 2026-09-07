---
name: math-audit-mip
description: SA3b — rigorous comparison of thesis equations vs master notebook code (code wins)
---

# Math audit for MIP formulations

## Triggers

- SA3b after SA2b when `packs` includes `optimization-or` and thesis contains MIP chapters.
- User requests “math audit”, “equations vs code”, or discrepancy list before paper Methods.
- Before claiming a constraint or objective in `paper/main.tex` matches implementation.

## Read order

1. Thesis LaTeX or PDF equations (read-only Overleaf/thesis project).
2. Master notebooks in `Thesis Code/` — **code is ground truth** per project policy.
3. `memory/thesis_model_registry.md` for model boundaries (MOD, SSS, SSSMP).
4. Prior `memory/math_corrections.md` or create writable section in `memoria_hallazgos/` equivalent.

## Steps

1. **Inventory equations:** list numbered constraints/objectives referenced in Results for enabled models only.
2. **Map to code:** for each equation, cite notebook cell or `codigo/` function implementing it (path + symbol names).
3. **Index sets:** verify ∀i∈V, ∀(i,j)∈A, ∀k∈K match Python set constructors (off-by-one, depot excluded twice).
4. **Big-M and units:** check scaling (km vs m, hours vs seconds, kWh vs %) — document conversion factors in audit table.
5. **Linearization:** identify if thesis shows nonlinear form but code uses linearized version — flag as `IMPLEMENTATION_LINEARIZATION`.
6. **Missing constraints:** code has constraint not in thesis → `THESIS_GAP`; thesis has unused equation → `THESIS_EXTRA`.
7. **Discrepancy severity:** `BLOCKER` (changes optimal value interpretation), `NOTATION`, `DOC_ONLY`.
8. **Output:** update `memory/math_corrections.md` (or agreed path) with table: id, thesis ref, code ref, status, fix owner.
9. **Paper policy:** Methods may cite corrected form; do not silently “fix” numbers in Results without SA4 join.

## Forbidden

- Declaring thesis right when code differs (policy: **code wins** for implementation truth).
- Editing master notebooks or thesis Overleaf (read-only archaeology).
- Inventing proofs or objective values to close gaps.
- Running full MIP solves during audit unless needed to validate a suspected scaling bug.

## Verify

- Audit table covers every active constraint family in `paper_strategy_brief` model list.
- Each `BLOCKER` has linked experiment id or `TBD` repro plan.
- No Spanish block pasted into `paper/main.tex` from audit notes.
- Closure: **SE TERMINÓ LA TAREA COMPLETA (SA3b)** → HANDOFF SA4; parallel SA3 may continue independently.
