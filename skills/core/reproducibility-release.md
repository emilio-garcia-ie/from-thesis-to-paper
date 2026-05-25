---
name: reproducibility-release
description: SA6 reproducibility and public release packaging — REPRODUCIBILITY.md, fixtures, smoke tests
---

# Reproducibility and release (SA6)

## Triggers

- Async after SA4 or SA5 refactor (`SA6 ~> after SA4 or SA5`).
- Before public GitHub release or journal data-availability statement.
- User asks for “repro pack”, “REPRODUCIBILITY”, “release checklist”.

## Read order

1. `memory/paper_strategy_brief.md` `evidence_path`.
2. `paper/REPRODUCIBILITY.md` if exists; `templates/memory/` repro template.
3. `scripts/run_tests.sh` and smoke test docs.
4. SA5 output if refactor created new `codigo/` modules.

## Steps

1. Document environment: Python version, Gurobi version (if used), key env vars — no secrets in repo.
2. List **golden fixtures** (e.g. locked experiment ids) and how to run smoke pipeline.
3. Explain discrepancy policies (catalog vs log) with reproducible commands, not invented numbers.
4. Separate **public** artifact list from **read-only** paths too large to ship.
5. Update `paper/REPRODUCIBILITY.md` and `memory/reproducibility_status.md`.
6. Run `./scripts/run_tests.sh smoke` when `codigo/` changed; record PASS/FAIL in status file.

## Forbidden

- Committing `.env`, Overleaf passwords, or license files with secrets.
- Copying 57GB verification trees into the release bundle.
- Claiming full replication if brief is `thesis_only_B` without stating limits.

## Verify

- `paper/REPRODUCIBILITY.md` exists and references smoke command.
- If `codigo/` touched in same tranche: smoke exit code 0.
- HANDOFF → SA13 or user release tag; does not block SA7–SA9 on fast path.
