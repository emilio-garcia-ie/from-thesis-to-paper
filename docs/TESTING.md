# Testing tiers (fttp framework)

Run from the **framework** repository root (`from-thesis-to-paper`):

```bash
./scripts/run_tests.sh {smoke|unit|integration|all}
```

Use the project virtualenv when present (`.venv/bin/python`); otherwise `python3`.

## Two tiers of “smoke”

| Where you run tests | What passes | Typical count |
|---------------------|-------------|---------------|
| **`from-thesis-to-paper` (this repo)** | Config schema, hooks delegation, venue profiles, `fttp.evidence` unit tests, optional LaTeX gate template | Framework-only (see `./scripts/run_tests.sh`) |
| **Consumer workspace** (e.g. PaperEPN `mi-investigacion-opt`) | Above **plus** Gurobi toy MIP, log lineage integration, paper pipeline fixtures, 18/18 consumer gate | Documented in that repo’s `docs/TESTING.md` |

**Do not** expect **18/18** or PaperEPN archaeology tests to run in CI for the framework repo alone. Those tests live in the user workspace that owns `experimentos/`, hooks scripts, and catalog data.

## Framework tiers

| Tier | Command | Gurobi needed? | Purpose |
|------|---------|----------------|---------|
| **smoke** | `./scripts/run_tests.sh smoke` | No | Fast: config, hooks schema, dummy hook scripts, evidence CSV validators |
| **unit** | `./scripts/run_tests.sh unit` | No | All tests under `tests/` (includes smoke-marked tests) |
| **integration** | `./scripts/run_tests.sh integration` | No in framework | Placeholder — run MIP/integration in consumer workspace |
| **all** | `./scripts/run_tests.sh all` | No in framework | smoke + full unit suite |

## Smoke composition (framework)

1. `tests/test_config.py` — config resolution and JSON load (`@pytest.mark.smoke`)
2. `tests/test_hooks_schema.py` — optional `hooks` / `venueProfiles` validation
3. `tests/test_run_hook.py` — subprocess hook delegation with fixture scripts
4. `tests/test_venue_profiles.py` — `activeVenue` / `resolve_active_main_tex`
5. `tests/test_evidence_*.py` — generic lineage CSV / Gurobi status map
6. `tests/test_latex_gates_template.py` — optional, when `FTTP_MAIN_TEX` points at a manuscript

## Consumer smoke (external)

After copying `examples/paperepn-external.config.json` → `fttp.config.json` in **your** workspace and setting `repoRoot` + `hooks` to real scripts:

```bash
cd /path/to/your-workspace
./scripts/run_tests.sh smoke   # e.g. 18/18 in PaperEPN when fully configured
```

Framework changes must pass **framework** smoke/unit before release; consumer smoke is the user’s regression gate.

## Agent gates (mandatory)

| Agent / build step | Required tier (framework maintainer) | Blocks HANDOFF if fail? |
|--------------------|--------------------------------------|-------------------------|
| fttp C1 hooks PR | `smoke` + `unit` in **from-thesis-to-paper** | **Yes** |
| SA0 consumer onboard | `fttp doctor` + consumer `smoke` if workspace has tests | doctor in framework: **Yes** |
| SA5 / SA11 code port | consumer `smoke` | **Yes** in workspace |
| SA9 | LaTeX compile (`fttp compile` or hook) | PDF/hook fail blocks |

**Closure rule:** record exit code in HANDOFF. If exit ≠ 0 → **TAREA INCOMPLETA** (include last 30 lines of test output).

## fttp CLI (after `pip install -e .`)

```bash
pip install -e .
FTTP_CONFIG=examples/paperepn-external.config.json python -m fttp doctor
python -m fttp tables    # runs hooks.tables under repoRoot when configured
./scripts/run_tests.sh smoke
```

Config: copy `templates/workspace.config.example.json` → `fttp.config.json` at **your** repo root, or set `FTTP_CONFIG` to an absolute path.
