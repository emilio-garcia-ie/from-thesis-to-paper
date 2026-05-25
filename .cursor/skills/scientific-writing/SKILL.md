---
name: scientific-writing
description: SA8 IMRaD LaTeX writer and SA10 on-demand peer review — English manuscript from signed brief
---

# Scientific writing (SA8 / SA10 peer review)

## Triggers

- **SA8:** After signed `memory/paper_strategy_brief.md` and approved glossary.
- **SA10 (on-demand):** User requests internal peer review of a section or full draft.
- Editing `paper/main.tex` or `paper/tables/*.tex`.

## Read order

1. `memory/paper_strategy_brief.md` — `narrative_arc`, `evidence_path`, `forbidden_claims`.
2. `memory/paper_narrative_map.md` or SA2 outline.
3. `memory/glossary_thesis_en.md` for model names.
4. `memory/venue_policy.md` for structure limits.
5. Catalog / discrepancy files — never invent table cells.

## Steps (SA8 writer)

1. **One section per pass** unless plan explicitly parallelizes non-overlapping files.
2. Default arc **`thesis_mirror`:** Results §5.1 (Cap.4-style) before §5.2 (Cap.5 / SSSMP).
3. Write native **English** IMRaD prose — do not paste Spanish thesis paragraphs.
4. Tables: `\input{tables/...}` fragments; cell values from signed evidence path only.
5. Mandatory intro phrase pattern: benchmark chapter results before multigraph extension (adapt wording, keep meaning).
6. Discrepancies (e.g. T002): document in `paper/REPRODUCIBILITY.md`, not Results footnotes unless brief says otherwise.

## Steps (SA10 peer review mode)

1. Read the same memory files; do not rewrite unless user asked for edits.
2. Produce structured review: Major / Minor / Clarity / Evidence gaps — cite labels `\ref{}` missing, unsupported claims, tier-B visibility.
3. Cross-check against `forbidden_claims` and venue page limits.
4. Output `memory/peer_review_<date>.md` or comment list in chat per user preference.
5. If blocking issues → recommend **TAREA INCOMPLETA** for submission clerk until fixed.

## Forbidden

- Claiming VRPLTT base is implemented when brief forbids it.
- Presenting SSSMP as proven before Cap.4 comparison tables in `thesis_mirror`.
- Spanish in `\section` body text.
- Auto-translating thesis without user trigger of translation rule.

## Verify

- `grep -n '\\\\section' paper/main.tex` shows English headings only (manual spot-check).
- Each cited table label exists or is marked `TBD` in prose.
- SA8 HANDOFF → SA9; SA10 HANDOFF → SA11 only if refactor fixes requested and pack enabled.
