---
name: narrative-interview
description: SA2 narrative interview — contributions, arc, forbidden claims before glossary and writing
---

# Narrative interview (SA2)

## Triggers

- After SA1 venue policy; before SA2b glossary and SA7 strategy on new papers.
- User says “narrative”, “contributions”, “story arc”, or disputes IMRaD order.

## Read order

1. `memory/venue_policy.md` — **G1-venue** must be approved before SA2 starts ([docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md)).
2. `memory/thesis_scientific_structure.md` or thesis outline cache (read-only).
3. `memory/paper_narrative_map.md` if present from prior work.
4. `docs/ARCHITECTURE.md` §5 fast path vs full SA chain.
5. `memory/user_approval_log.md` — write **G2-narrative** row after user approval (below).

## Steps

1. **Ask structured questions** (record answers in chat; user may answer ES or EN):
   - Main contribution in one sentence?
   - Benchmark-before-extension ordering required?
   - What must **not** be claimed (e.g. unimplemented baselines)?
2. Propose `narrative_arc`: `thesis_mirror` | `contribution_first` | `integrated` — default `thesis_mirror` unless user overrides.
3. List **forbidden_claims** explicitly (VRPLTT base implemented, SSSMP before Cap.4 tables, etc.).
4. Draft outline bullets for Introduction and Results order; no LaTeX yet.
5. Write `memory/narrative_interview.md` with dated Q&A and recommended arc.
6. If user cannot decide arc → stop with **ASK USER**; do not proceed to SA8.
7. Run **G2-narrative** AUDIT / APPROVE before HANDOFF to SA2b (below).

## G2-narrative — AUDIT / APPROVE (mandatory)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md). **Blocks SA2b and SA7** until approved in `memory/user_approval_log.md`.

After `memory/narrative_interview.md` is written:

```text
AUDIT: G2-narrative — review memory/narrative_interview.md
Checklist:
- One-sentence main contribution stated
- narrative_arc chosen (thesis_mirror | contribution_first | integrated)
- forbidden_claims list explicit (unimplemented baselines, ordering traps)
- Results / Introduction outline bullets present; no LaTeX body yet
APPROVE_ASK: Confirm this story matches your thesis and journal intent. Reply APPROVED: G2-narrative (EN) or APROBADO: G2-narrative (ES) or corrections.
```

On user approval: update row **`G2-narrative`** in `memory/user_approval_log.md` — `user_status`, `approved_at` (ISO-8601), `artifact_paths`, `notes`.

**Without approval:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA2b ni SA7 — missing approved row for G2-narrative
```

## Forbidden

- Writing full `paper/main.tex` sections in SA2.
- Translating entire thesis chapters into the interview file (English summaries only).
- Skipping forbidden-claims list.

## Verify

- `memory/narrative_interview.md` contains `narrative_arc` and `forbidden_claims` sections.
- `memory/user_approval_log.md` has **G2-narrative** `approved` (or `approved_with_edits`).
- HANDOFF → SA2b (terminology) **only after G2-narrative approved**; SA7 if glossary already current per orchestration plan.
