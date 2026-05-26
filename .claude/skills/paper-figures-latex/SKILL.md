---
name: paper-figures-latex
description: SA9 figures, table fragments, LaTeX build verify — pipeline and labels
---

# Paper figures and LaTeX verify (SA9)

## Triggers

- After SA8 first Results prose or when table fragments exist.
- User asks to build PDF, fix figures, or verify `\ref{}`.
- Before SA12 Overleaf sync or SA13 submission clerk.

## Read order

1. `memory/paper_strategy_brief.md` figure flags (multigraph schematic, maps, route example).
2. `memory/venue_policy.md` and `paper/JOURNAL_GUIDELINES.md` — **figure/table limits**, resolution, color policy, supplementary rules ([docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md) **G1-venue** must be approved).
3. Active manuscript: `paper.mainTex` or `paper.venueProfiles[activeVenue].mainTex` from `fttp.config.json` (use `fttp doctor` to print resolved path).
4. `docs/PAPER_PRODUCTION_PIPELINE.md` — `fttp figures` and `fttp compile` delegate to `hooks.figures` / `hooks.compile` or venue `build` under `repoRoot`.
5. Consumer `scripts/run_tests.sh smoke` if touching generation scripts; framework maintainers run `./scripts/run_tests.sh smoke` in **from-thesis-to-paper** after CLI changes.
6. Optional LaTeX gates: `FTTP_MAIN_TEX=/path/to/main.tex pytest tests/test_latex_gates_template.py -m smoke` (no `\codepath`, no `lineageDiscrepancy` in body, thesis cite keys).
7. `memory/user_approval_log.md` — write **G9-figures** after build audit (below).

## Venue figure limits (mandatory check)

Before finalizing figures or submission PDF:

1. Read **Constraints** and figure bullets from `memory/venue_policy.md` (page count, max figures, color vs grayscale, min DPI).
2. Cross-check `paper/JOURNAL_GUIDELINES.md` checklist — same limits; if conflict, **venue_policy wins** and note in `memory/figures_latex_report.md`.
3. Count in-manuscript figures + tables against limits; move overflow to supplementary only if venue policy allows and brief agrees.
4. Document any **TBD** figure placeholders with caption note — no silent low-res assets in submission build.

## Steps

1. **Figure manifest:** list each figure file, source script, and target label (`fig:...`).
2. Generate or copy figures into `paper/figures/` (or configured path) — no placeholder images in submission build without `TBD` caption note.
3. Ensure table fragments compile: `python -m fttp compile` (venue build hook) or `latexmk` on the active `mainTex`; capture log errors.
4. Fix broken `\ref{}` / missing labels; do not change numeric table cells in this pass unless SA4 signed.
5. Run legend/smoke tests if repo provides `scripts/run_tests.sh smoke` after codegen changes.
6. Write `memory/figures_latex_report.md` with PASS/FAIL, venue limit compliance, and log excerpt ≤30 lines.
7. Run **G9-figures** AUDIT / APPROVE before HANDOFF to SA12 or SA13 (below).

## G9-figures — AUDIT / APPROVE (mandatory)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md). **Blocks SA12 and SA13** until approved.

After `paper/tables/*.tex`, `paper/figures/*`, and optional `paper/main.pdf` build:

```text
AUDIT: G9-figures — review paper/tables/*.tex, paper/figures/*, figures_latex_report.md, PDF if built
Checklist:
- Labels match signed brief; \ref{} resolve in touched sections
- Table numbers match catalog / approved DISCREPANCY policy (no invented cells)
- Figure count and resolution within venue_policy / JOURNAL_GUIDELINES limits
APPROVE_ASK: Confirm figures and tables are submission-ready. Reply APPROVED: G9-figures (EN) or APROBADO: G9-figures (ES) or corrections.
```

On user approval: update row **`G9-figures`** in `memory/user_approval_log.md`.

**Without approval:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA12 ni SA13 — missing approved row for G9-figures
```

## Forbidden

- Editing thesis Overleaf project (read-only); paper project only for SA12.
- Inventing figure paths that do not exist on disk.
- Full re-write of IMRaD prose (scope is figures + build + labels).

## Verify

- `paper/main.pdf` builds OR log shows only known non-blocking warnings documented in report.
- All figure/table `\ref{}` in touched sections resolve.
- Venue figure/table limits checked against `venue_policy.md` and `JOURNAL_GUIDELINES.md` (noted in report).
- `memory/user_approval_log.md` has **G9-figures** `approved` before HANDOFF.
- HANDOFF → SA12 (optional Overleaf) or SA13 when PDF OK and G9 approved.
