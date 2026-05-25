---
name: venue-submission-policy
description: SA1 venue scout — journal constraints, page limits, data/code policy, APC
---

# Venue submission policy (SA1)

## Triggers

- Before paper strategy (SA7) or first `main.tex` structure pass.
- User names a target journal, conference, or “working paper only”.
- Prompt header includes SA1 or `venue-submission-policy`.

## Read order

1. `memory/workspace_intake.md` (SA0 output).
2. User-supplied venue URL or `paper/JOURNAL_GUIDELINES.md` if already drafted.
3. `skills/core/paper-strategy.md` cross-check after policy file exists (do not run SA7 before SA1 on greenfield projects).

## Steps

1. **Identify venue class:** journal / conference / thesis condensation / internal report.
2. **Extract constraints:** word/page limits, abstract structure, reference style, figure resolution, supplementary rules.
3. **Data & code policy:** repository requirement, ORCID, conflict statements, preprint rules.
4. **Costs & timeline:** APC if applicable; realistic submission window → feeds `evidence_path` in SA7.
5. Write `memory/venue_policy.md` with sections: Constraints, Required sections, Forbidden in this venue, Citation style, Open data.
6. Flag blockers (e.g. double-blind → no identifying `\texttt{path}` in PDF).

## Forbidden

- Assuming Elsevier/Springer defaults without a source URL or user confirmation.
- Editing `paper/main.tex` in SA1 (policy only).
- Promising replication the brief has not signed.

## Verify

- `memory/venue_policy.md` exists and mentions page/limit or states “no limit found — ASK USER”.
- Policy file links to SA7 brief fields (`evidence_path`, figure limits) without duplicating strategy decisions.
- HANDOFF → SA2 (narrative interview).
- Record venue URL in `memory/venue_policy.md` header for traceability.
