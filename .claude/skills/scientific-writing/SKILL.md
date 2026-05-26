---
name: scientific-writing
description: SA8 IMRaD LaTeX writer and SA10 on-demand peer review — English manuscript from signed brief
---

# Scientific writing (SA8 / SA10 peer review)

## Triggers

- **SA8:** After signed `memory/paper_strategy_brief.md` and approved glossary.
- **SA10 (on-demand):** User requests internal peer review of a section or full draft.
- Editing `paper/main.tex` or `paper/tables/*.tex`.

## Preconditions (onboarding v2)

- **G7-strategy** and **G1-venue** must have `user_status: approved` (or `approved_with_edits`) in `memory/user_approval_log.md` before SA8 starts.
- **G2b-glossary** approved when the workflow profile includes it.
- **G4-evidence** approved when `workflowProfile` is `paper_audit`, `paper_audit_repro`, or `full_pipeline` (waived for `paper_only` — note in log).
- Load `writingMode` from `fttp.config.json` (or `writing_mode` in signed brief); see **Writing mode** below.

## Read order

1. `memory/paper_strategy_brief.md` — `narrative_arc`, `evidence_path`, `writing_mode`, `forbidden_claims`.
2. `memory/paper_narrative_map.md` or SA2 outline.
3. `memory/glossary_thesis_en.md` for model names.
4. `memory/venue_policy.md` for structure limits.
5. `memory/thesis_experiment_catalog.md`, `memory/discrepancy_registry.md` (or `memory/evidence_discrepancies.md`) — never invent table cells; use `TBD` or `DISCREPANCY` per join audit.
6. `memory/provenance_map.md` when `writing_mode` is `thesis_adapt` or `hybrid` (see below).

## Writing mode (`writingMode` / `writing_mode`)

Set in SA0 (`fttp.config.json`) and copied into the signed brief. Drives how prose is produced:

| Mode | Behavior | Provenance map |
|------|----------|----------------|
| **`thesis_adapt`** | Extract and condense defended thesis prose; preserve voice; English IMRaD output | **Required** — maintain `memory/provenance_map.md` |
| **`compose`** | Draft primarily from brief, catalog, and glossary; higher generic-tone risk | Optional unless brief marks hybrid sections |
| **`hybrid`** | Per-section choice (adapt vs compose); record which blocks are adapted | **Required** for every `thesis_adapt` block |

### `memory/provenance_map.md` (thesis_adapt / hybrid)

For each adapted paragraph or subsection in `paper/main.tex`:

1. Record **paper anchor** (section label, approximate lines, or stable comment id).
2. Record **thesis source** (chapter/section, Overleaf path, or thesis PDF page — read-only archaeology only).
3. Note **adaptation type**: condense | restructure | terminology swap (glossary EN).
4. Flag **numeric cells** as `catalog` | `TBD` | `DISCREPANCY` — never claim a number without a catalog row or approved discrepancy policy.

Update the map in the **same pass** as the prose edit. G8-prose audit includes this file when mode is `thesis_adapt` or `hybrid`.

## Numeric evidence (mandatory)

- **Do not invent** objectives, gaps, runtimes, instance counts, or table cells.
- Published numbers must trace to **signed** `evidence_path`, catalog rows, or user-approved `DISCREPANCY` policy in the brief / `memory/discrepancy_registry.md`.
- Use **`TBD`** in prose and table fragments when the join audit has no authoritative cell yet.
- Use **`DISCREPANCY`** (and document in `paper/REPRODUCIBILITY.md`) when sources disagree — never silently pick the favorable value.

## Steps (SA8 writer)

1. **One section per pass** unless plan explicitly parallelizes non-overlapping files.
2. Default arc **`thesis_mirror`:** Results §5.1 (Cap.4-style) before §5.2 (Cap.5 / SSSMP).
3. Write native **English** IMRaD prose — do not paste Spanish thesis paragraphs.
4. Tables: `\input{tables/...}` fragments; cell values from signed evidence path only.
5. Mandatory intro phrase pattern: benchmark chapter results before multigraph extension (adapt wording, keep meaning).
6. Discrepancies (e.g. T002): document in `paper/REPRODUCIBILITY.md`, not Results footnotes unless brief says otherwise.
7. Respect `writing_mode`: adapt with provenance map, or compose from brief only where mode allows.
8. After each section batch, run **G8-prose** closure (below) before HANDOFF to SA9.

## G8-prose — AUDIT / APPROVE (mandatory)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md). Blocks SA9 until the agreed section batch is approved.

After updating `paper/main.tex` (and `memory/provenance_map.md` when applicable):

```text
AUDIT: G8-prose — review paper/main.tex section(s) [list sections]; provenance_map if thesis_adapt/hybrid
Checklist:
- English IMRaD; no Spanish in \section body
- No forbidden_claims from brief / G2
- Table refs exist or prose says TBD; numbers match catalog / approved DISCREPANCY policy
- Adapted paragraphs traceable in provenance_map (if applicable)
APPROVE_ASK: Confirm prose reflects your voice and brief. Reply APPROVED: G8-prose (EN) or APROBADO: G8-prose (ES) or corrections.
```

On user approval: append or update row **`G8-prose`** in `memory/user_approval_log.md` — `user_status`, `approved_at` (ISO-8601), `artifact_paths`, `notes`.

**Without approval:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA9 — missing approved row for G8-prose
```

Partial multi-session work: log which sections are approved in `notes`; do not HANDOFF full SA9 until all planned sections have G8-prose approved or user waives in chat.

## Steps (SA10 peer review mode)

1. Read the same memory files; do not rewrite unless user asked for edits.
2. Produce structured review: Major / Minor / Clarity / Evidence gaps — cite labels `\ref{}` missing, unsupported claims, tier-B visibility.
3. Cross-check against `forbidden_claims` and venue page limits.
4. Output `memory/peer_review_<date>.md` or comment list in chat per user preference.
5. If blocking issues → recommend **TAREA INCOMPLETA** for submission clerk until fixed.

## Forbidden

- Inventing or rounding numeric results not in catalog / join audit / approved discrepancy policy.
- Claiming VRPLTT base is implemented when brief forbids it.
- Presenting SSSMP as proven before Cap.4 comparison tables in `thesis_mirror`.
- Spanish in `\section` body text.
- Auto-translating thesis without user trigger of translation rule.

## Verify

- `grep -n '\\\\section' paper/main.tex` shows English headings only (manual spot-check).
- Each cited table label exists or is marked `TBD` in prose.
- `memory/user_approval_log.md` has **G8-prose** `approved` for the section batch before HANDOFF → SA9.
- `memory/provenance_map.md` exists and is current when `writing_mode` ∈ {`thesis_adapt`, `hybrid`}.
- SA8 HANDOFF → SA9 only after G8-prose approved; SA10 HANDOFF → SA11 only if refactor fixes requested and pack enabled.
