---
name: submission-clerk
description: SA13 submission clerk — checklist, anonymization, PDF parity, portal-ready bundle
---

# Submission clerk (SA13)

## Triggers

- After SA9 PDF builds and optional SA12 sync.
- User says “ready to submit”, “submission package”, “SA13”.
- Venue deadline within user-stated window.

## Read order

1. `memory/venue_policy.md` (SA1).
2. `memory/paper_strategy_brief.md` signed.
3. `memory/figures_latex_report.md` and latest `paper/main.pdf`.
4. `paper/REPRODUCIBILITY.md` and conflict-of-interest templates if required.

## Steps

1. **Submission checklist** from venue policy: files, word count, blind rules, highlights, graphical abstract.
2. Verify PDF metadata: no broken links, fonts embedded, figures ≥ minimum DPI.
3. Anonymization pass if double-blind: strip identifying paths, acknowledgments per policy.
4. Match supplement list to actual files on disk; mark missing as `TBD`.
5. Write `memory/submission_checklist.md` with tick boxes PASS/FAIL/N/A.
6. If any FAIL on evidence or repro → **BLOQUEADO** until SA8/SA6 fix — do not claim ready.

## Forbidden

- Submitting on behalf of user without explicit “go” instruction.
- Hiding `DISCREPANCY` items not disclosed in supplement or REPRODUCIBILITY.
- Zipping read-only verification trees into submission upload.

## Verify

- `memory/submission_checklist.md` all required rows PASS or user-waived in writing.
- PDF file size and page count within venue limits or flagged.
- Closure: **SE TERMINÓ LA TAREA COMPLETA (SA13)** when checklist complete.
