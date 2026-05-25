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
   - Cap.4 / Cap.5 table scope (full vs summary rows).
   - `t002_policy` and other named discrepancy policies.
2. List `forbidden_claims` copied from SA2 plus any new from SA4.
3. Require `approved_by: user` and date before marking brief **signed**.
4. Write `memory/paper_strategy_brief.md` using template sections from `templates/memory/`.
5. If user wants `recompute_A` but Gurobi missing → **TAREA INCOMPLETA** or downgrade path with user OK.

## Forbidden

- Editing verification trees or kicking off 57GB batch reruns without explicit `recompute_A`.
- Changing signed brief fields in downstream agents without user OK.
- Embedding optimization-or pack instructions (point to pack manifest only).

## Verify

- Brief contains signed `evidence_path` and `narrative_arc`.
- HANDOFF → SA8 (writer) and SA9 (figures) after brief signed; SA13 only after SA9 per fast path.
