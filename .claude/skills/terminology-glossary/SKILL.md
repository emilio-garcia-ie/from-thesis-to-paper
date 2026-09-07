---
name: terminology-glossary
description: SA2b thesis term mining and English glossary — user confirms before SA8 writing
---

# Terminology glossary (SA2b)

## Triggers

- After SA2 narrative interview; **before** SA8 scientific writing.
- Spanish thesis terms appear in memory or Overleaf cache.
- User requests glossary or “EN terms for models”.

## Read order

1. `memory/narrative_interview.md` and `memory/thesis_model_registry.md` (banner-only Spanish cells OK).
2. `templates/memory/glossary_thesis_en_TEMPLATE.md`.
3. `docs/TRANSLATION_GUIDE.md` Maintenance section for existing rows.
4. `memory/venue_policy.md` for discipline-specific naming (OR vs engineering).

## Steps

1. **Mine terms:** model names, Spanish acronyms, city/instance names, constraint labels — table format `| ES source | EN proposal | notes |`.
2. Mark uncertain rows `TBD` — do not guess journal-standard abbreviations.
3. Propose consistent EN macros / `\newcommand` names for LaTeX (align with existing `paper/main.tex` if present).
4. **ASK USER** to confirm or correct EN column before marking glossary `approved`.
5. Write `memory/glossary_thesis_en.md` (or path from config); set `approved_by` and date when user OK.
6. Optional: append ≤3 rows to `docs/TRANSLATION_GUIDE.md` Maintenance (append-only).

## Forbidden

- Auto-approving glossary without user confirmation.
- Replacing Spanish cells inside `thesis_*` catalog tables (banner-only policy).
- Bulk machine-translating 200+ table rows into glossary.

## Verify

- Glossary file exists; ≥10 terms or explicit “small thesis — N terms”.
- `approved_by: user` present before HANDOFF to SA7/SA8 writers.
- No Spanish body text in new `skills/` or `docs/` files.
