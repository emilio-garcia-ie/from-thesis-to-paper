---
name: narrative-interview
description: SA2 narrative interview — contributions, arc, forbidden claims before glossary and writing
---

# Narrative interview (SA2)

## Triggers

- After SA1 venue policy; before SA2b glossary and SA7 strategy on new papers.
- User says “narrative”, “contributions”, “story arc”, or disputes IMRaD order.

## Read order

1. `memory/venue_policy.md`.
2. `memory/thesis_scientific_structure.md` or thesis outline cache (read-only).
3. `memory/paper_narrative_map.md` if present from prior work.
4. `docs/ARCHITECTURE.md` §5 fast path vs full SA chain.

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

## Forbidden

- Writing full `paper/main.tex` sections in SA2.
- Translating entire thesis chapters into the interview file (English summaries only).
- Skipping forbidden-claims list.

## Verify

- `memory/narrative_interview.md` contains `narrative_arc` and `forbidden_claims` sections.
- HANDOFF → SA2b (terminology) or SA7 if glossary already current (orchestration plan decides).
