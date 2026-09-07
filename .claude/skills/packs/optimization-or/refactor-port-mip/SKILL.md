---
name: refactor-port-mip
description: Port validated notebook MIP workflows to modular codigo/ — read-only sources, .env parameters
---

# Refactor port for MIP pipelines

## Triggers

- SA5 or SA11 after SA4 gate; user approves porting a validated notebook loop to `codigo/`.
- Reproducibility plan requires end-to-end script instead of twin notebook execution.
- Fixing refactor regressions (SA11) with pack enabled.

## Read order

1. Twin vs master notebook report from SA3 (which notebook has the real loop).
2. `memory/math_corrections.md` — do not port known-wrong thesis-only equations over code.
3. `codigo/` existing layout and `scripts/run_tests.sh` expectations.
4. `.env.example` / repo `.env` for Gurobi license path and data roots (never commit secrets).

## Steps

1. **Scope one workflow per pass:** e.g. single model id + scenario family — avoid mega-module.
2. **Read-only source:** copy logic from master/twin notebook mentally; implement fresh `.py` under `codigo/`.
3. **Module split:** `data_loader.py`, `model_build.py`, `solve.py`, `io_export.py` (names match repo conventions).
4. **Parameters:** move paths, time limits, gap to `.env` or CLI args — no machine-specific absolutes in git.
5. **Outputs:** write only under `experimentos/` or configured writable root; mirror thesis artifact names if needed for diff.
6. **Try/except:** wrap solve loop per instance; log failure id; continue batch for paper tables.
7. **Tests:** extend smoke fixtures — mock small instance without full Gurobi when possible.
8. **Integration:** if Gurobi available, `./scripts/run_tests.sh integration` per orchestration plan.
9. Document entrypoint in `paper/REPRODUCIBILITY.md` or `memory/` repro note.

## Forbidden

- Modifying `Thesis Code/` master notebooks or OneDrive verification outputs.
- Copy-pasting 57GB trees into repo.
- Porting without user approval when plan says archaeology-only.
- HANDOFF to SA8 with new numbers before SA4 join marks cells OK.

## Verify

- `./scripts/run_tests.sh smoke` exit **0** (mandatory before HANDOFF per fttp-non-negotiables).
- New modules importable: `python -c "import codigo"` or package path documented.
- One golden instance reproduces locked objective within tolerance or documents `DISCREPANCY`.
- Closure SA5 → SA6 reproducibility; SA11 → re-run smoke + user confirmation.
