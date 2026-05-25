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
2. `paper/main.tex` structure and existing `\includegraphics` paths.
3. `docs/PAPER_PRODUCTION_PIPELINE.md` for `fttp figures` / `compile` commands when CLI exists.
4. `scripts/run_tests.sh smoke` if touching generation scripts under `codigo/`.

## Steps

1. **Figure manifest:** list each figure file, source script, and target label (`fig:...`).
2. Generate or copy figures into `paper/figures/` (or configured path) — no placeholder images in submission build without `TBD` caption note.
3. Ensure table fragments compile: run `pdflatex` or project compile script; capture log errors.
4. Fix broken `\ref{}` / missing labels; do not change numeric table cells in this pass unless SA4 signed.
5. Run legend/smoke tests if repo provides `scripts/run_tests.sh smoke` after codegen changes.
6. Write `memory/figures_latex_report.md` with PASS/FAIL and log excerpt ≤30 lines.

## Forbidden

- Editing thesis Overleaf project (read-only); paper project only for SA12.
- Inventing figure paths that do not exist on disk.
- Full re-write of IMRaD prose (scope is figures + build + labels).

## Verify

- `paper/main.pdf` builds OR log shows only known non-blocking warnings documented in report.
- All figure/table `\ref{}` in touched sections resolve.
- HANDOFF → SA12 (optional Overleaf) or SA13 when PDF OK.
