# Testing tiers (fttp / PaperEPN)

> Aligns with [`.cursor/plans/from-thesis-to-paper_orchestration.plan.md`](../.cursor/plans/from-thesis-to-paper_orchestration.plan.md) test gates.

Run from repository root:

```bash
./scripts/run_tests.sh {smoke|unit|integration|all}
```

Use the project virtualenv when present (`.venv/bin/python`); otherwise `python3`.

## Tiers

| Tier | Command | Gurobi needed? | Purpose |
|------|---------|----------------|---------|
| **smoke** | `./scripts/run_tests.sh smoke` | No (or skip toy MIP) | Fast sanity: config load, log lineage, paper fixtures, legend figure |
| **unit** | `./scripts/run_tests.sh unit` | No | Pure Python tests under `tests/unit/` |
| **integration** | `./scripts/run_tests.sh integration` | Yes | Golden MIP / fixture solves |
| **all** | `./scripts/run_tests.sh all` | Yes for integration | smoke subset + full unit + integration |

## Smoke composition (PaperEPN)

1. `tests/test_config.py` — `fttp` config resolution and JSON load
2. `tests/unit/test_gurobi_smoke.py` — optional Gurobi import / toy MIP (`-m smoke`)
3. `tests/test_log_lineage.py` — log lineage helpers (`-m smoke`)
4. `tests/test_paper_pipeline_smoke.py` — fixtures, legend figure, bibliography map (`-m smoke`)

## Agent gates (mandatory)

| Agent / build step | Required tier | Blocks HANDOFF if fail? |
|--------------------|---------------|-------------------------|
| B7 (P6 Python fttp) | `smoke` | **Yes** |
| B12 | `smoke` (+ optional `all`) | **Yes** |
| SA0 | `fttp doctor` (P7); `smoke` if workspace has `tests/` | doctor: **Yes** |
| SA4 | `smoke` if `codigo/` or `tests/` touched | **Yes** |
| SA5 / SA11 | `smoke`; `integration` if MIP changed | **Yes** |
| SA9 | LaTeX compile (`fttp compile` or latexmk) | PDF fail blocks |
| SA13 | `smoke` minimum in checklist | checklist item |

**Closure rule:** record exit code in HANDOFF. If exit ≠ 0 → **TAREA INCOMPLETA** (include last 30 lines of test output).

## fttp CLI (after `pip install -e .`)

```bash
pip install -e .
python -m fttp tables    # stub; needs fttp.config.json or FTTP_CONFIG
./scripts/run_tests.sh smoke
```

Config: copy `templates/workspace.config.example.json` → `fttp.config.json` at repo root, or set `FTTP_CONFIG` to an absolute path.
