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

1. `memory/workspace_intake.md` and `fttp.config.json` — `readOnlyRoots`, **`copyPolicy`**.
2. `memory/thesis_experiment_run_artifacts.md` or template (artifact glossary).
3. Excel/CSV summaries under verification trees (**search, do not cat huge logs**).
4. Master notebooks in `Thesis Code/` (read-only).
5. [docs/WORKSPACE_MODEL.md](../../docs/WORKSPACE_MODEL.md) §4 — copy manifest (what may enter writable `experimentos/evidence/`).

## Copy policy manifest (`copyPolicy`)

Evidence enters the **writable** workspace by **copy or extract**, never by editing read-only roots.

| Config field | Role |
|--------------|------|
| `copyPolicy.maxArtifactMb` | Refuse or warn before copying a single file above the limit (default often 500) |
| `copyPolicy.allowSymlinks` | Default `false` — prefer real files for clones/CI |

**What may be copied** (from `readOnlyRoots` → workspace):

| Source (RO) | Typical destination | Notes |
|-------------|---------------------|--------|
| Excel/CSV summaries | `experimentos/evidence/` | Prefer over raw multi-GB logs |
| Small log tails / scripted extracts | `experimentos/evidence/` | Token-safe excerpts only |
| Catalog-facing row metadata | `memory/thesis_experiment_catalog.md` | Agent-maintained; tag `TBD` where missing |

**Never:** edit verification trees, master notebooks, or thesis Overleaf; do not copy full multi-GB verification trees wholesale.

Record planned or completed copies in `memory/evidence_archaeology_report.md` (path, size, tier). Discrepancies discovered during copy point to SA4 / `memory/discrepancy_registry.md` — not hidden at SA3.

## G4-evidence (preparation only at SA3)

SA3 is **read-only archaeology** — there is **no user approval gate at SA3**. Mandatory checkpoint **G4-evidence** runs in **SA4** after catalog and join artifacts exist ([docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md)).

At SA3: ensure every table id the paper will need is listed with `OK` | `TBD` | `DISCREPANCY` so SA4 can surface them for user visibility before SA7.

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
- Copy manifest respected: no RO edits; copies within `copyPolicy.maxArtifactMb`.
- Token-safe: no full log file reads into model context.
- HANDOFF → SA4 (join auditor); SA3b optional in parallel if pack enabled. **Do not** claim G4-evidence approved at SA3.
