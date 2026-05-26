---
name: paper-strategy
description: SA7 paper strategist — signed brief, narrative arc, evidence_path, table policy
---

# Paper strategy (SA7)

## Triggers

- After SA4 join audit; **before** SA8 long LaTeX writing or bulk table generation.
- User asks “strategy brief”, “what tables go in the paper”, “thesis_mirror vs contribution_first”.
- Any agent about to run Gurobi recompute loops.

## Read order

1. `memory/narrative_interview.md`, `memory/venue_policy.md`, `memory/evidence_discrepancies.md`.
2. `memory/glossary_thesis_en.md` (must be user-approved).
3. Legacy `memory/paper_strategy_brief.md` if migrating from PaperEPN — merge, do not silently delete decisions.

## Steps

1. Run decision checklist (record in brief):
   - `narrative_arc` (default `thesis_mirror`).
   - `evidence_path`: `recompute_A` | `thesis_only_B` | `hybrid_B_plus`.
   - **`writing_mode`**: `thesis_adapt` | `compose` | `hybrid` — copy from `fttp.config.json` `writingMode` unless user overrides in SA0; SA8 prose and provenance rules depend on this field.
   - Cap.4 / Cap.5 table scope (full vs summary rows).
   - `t002_policy` and other named discrepancy policies.
2. List `forbidden_claims` copied from SA2 plus any new from SA4.
3. Align claims with **G2-narrative** and **G4-evidence** (when profile requires G4): no strategy that hides `TBD`/`DISCREPANCY` rows.
4. Require `approved_by: user` and date before marking brief **signed** (agent draft ≠ user sign-off).
5. Write `memory/paper_strategy_brief.md` using template sections from `templates/memory/`.
6. If user wants `recompute_A` but Gurobi missing → **TAREA INCOMPLETA** or downgrade path with user OK.
7. Issue **G7-strategy** AUDIT / APPROVE before any HANDOFF to SA8 (below).

## G7-strategy — AUDIT / APPROVE (mandatory)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md). **Blocks SA8** until approved in `memory/user_approval_log.md`.

After the brief is written and internally consistent:

```text
AUDIT: G7-strategy — review memory/paper_strategy_brief.md
Checklist:
- evidence_path and allowed tables explicit
- writing_mode recorded (thesis_adapt | compose | hybrid)
- narrative_arc and forbidden_claims align with G2-narrative
- Discrepancy / TBD policies align with G4-evidence when profile includes G4
APPROVE_ASK: Confirm strategy before prose writing. Reply APPROVED: G7-strategy (EN) or APROBADO: G7-strategy (ES) or corrections.
```

On user approval: update row **`G7-strategy`** in `memory/user_approval_log.md` — `user_status`, `approved_at` (ISO-8601), `artifact_paths`, `notes`.

**Without approval:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA8 — missing approved row for G7-strategy
```

Do not HANDOFF to SA8 based on agent-only `approved_by` in the brief YAML — the log row is the gate.

## Forbidden

- Editing verification trees or kicking off 57GB batch reruns without explicit `recompute_A`.
- Changing signed brief fields in downstream agents without user OK.
- Embedding optimization-or pack instructions (point to pack manifest only).

## Verify

- Brief contains signed `evidence_path`, `narrative_arc`, and **`writing_mode`**.
- `memory/user_approval_log.md` has **G7-strategy** `approved` (or `approved_with_edits`).
- HANDOFF → SA8 (writer) **only after G7-strategy approved**; SA9 (figures) may plan in parallel but must not publish table numbers contradicting the signed brief; SA13 only after SA9 per fast path.
