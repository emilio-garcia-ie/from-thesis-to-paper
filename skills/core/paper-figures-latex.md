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
2. Active manuscript: `paper.mainTex` or `paper.venueProfiles[activeVenue].mainTex` from `fttp.config.json` (use `fttp doctor` to print resolved path).
3. `docs/PAPER_PRODUCTION_PIPELINE.md` — `fttp figures` and `fttp compile` delegate to `hooks.figures` / `hooks.compile` or venue `build` under `repoRoot`.
4. Consumer `scripts/run_tests.sh smoke` if touching generation scripts; framework maintainers run `./scripts/run_tests.sh smoke` in **from-thesis-to-paper** after CLI changes.
5. Optional LaTeX gates: `FTTP_MAIN_TEX=/path/to/main.tex pytest tests/test_latex_gates_template.py -m smoke` (no `\codepath`, no `lineageDiscrepancy` in body, thesis cite keys).

## Steps

1. **Figure manifest:** list each figure file, source script, and target label (`fig:...`).
2. Generate or copy figures into `paper/figures/` (or configured path) — no placeholder images in submission build without `TBD` caption note.
3. Ensure table fragments compile: `python -m fttp compile` (venue build hook) or `latexmk` on the active `mainTex`; capture log errors.
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
