---
name: mip-modeling-gurobi
description: MIP build, parameterize, solve, and re-solve with gurobipy or gurobi_cl — no GurobiMCP
---

# MIP modeling with Gurobi

## Triggers

- Building or reviewing a mixed-integer program for routing, scheduling, or facility location.
- User mentions `gurobipy`, `gurobi_cl`, `.lp` export, incumbent/gap, or SA5/SA11 refactor of solver code.
- Re-solving a staged `modelo.lp` from a read-only verification folder.

## Read order

1. `workspace.config.json` / `fttp.config.json` — confirm `packs` includes `optimization-or`.
2. Master notebook or `codigo/` module under **read-only** thesis roots (compare structure only).
3. `memory/thesis_model_registry.md` for model ids (MOD, SSS, SSSMP).
4. Instance JSON (`*__ins_*.json`) for parameters — never invent demands or battery caps.

## Steps

1. **Separate data from model:** load instance parameters from JSON; keep sets/parameters out of hard-coded notebook cells.
2. **Indexing discipline:** document node sets (depot, customers, charging), arc sets (simple vs multigraph layer), vehicle index — match thesis notation in comments.
3. **Build pattern (Python):** `gp.Model()`, `addVars` / `addConstrs`, objective sense and weights aligned with thesis (distance, time, energy).
4. **Export for audit:** write `modelo.lp` or `model.write()` to writable `experimentos/` only — never overwrite OneDrive run folders.
5. **Solve:** set `TimeLimit`, `MIPGap`, `Threads`; log `ModelName`, `NumVars`, `NumConstrs` at start.
6. **CLI path:** `gurobi_cl modelo.lp` when Python env unavailable; capture stdout to a new file under writable tree.
7. **Post-solve:** read `ObjVal`, `MIPGap`, `Runtime`, termination (`OPTIMAL`, `TIME_LIMIT`, `INFEASIBLE`) — map to catalog columns.
8. **Re-solve guard:** if golden row `golden_locked=Y`, compare objective hash before replacing catalog values.

## Forbidden

- Adding or configuring **GurobiMCP** (not part of fttp).
- Solving inside read-only verification trees.
- Silently changing objective sense or unit scaling to match a thesis typo.
- Claiming optimality without termination status from log or solver API.

## Verify

- Model builds without exception on a **smoke** instance (fixture or smallest `n_clients` case).
- `./scripts/run_tests.sh smoke` passes when `codigo/` changed (repo policy).
- LP path recorded in lineage CSV when applicable; objective matches log within catalog tolerance or tagged `DISCREPANCY`.
- HANDOFF → SA4 join audit or SA6 reproducibility when solve artifacts are new.
