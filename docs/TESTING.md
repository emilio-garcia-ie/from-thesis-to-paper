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

## Manual SA0 dry-run (recommended)

When you change onboarding, entry files, or guardrails, do a manual **SA0** dry-run in a fresh agent session to confirm the user-facing flow did not regress.

| Dry-run mode | Where | What you verify |
|-------------|-------|-----------------|
| **`FRAMEWORK_SMOKE`** | `REPO_FTTP` | No thesis paths requested; scaffolding/doctor paths are sane; framework smoke/unit still pass |
| **`CONSUMER_ONBOARD`** | A real paper workspace (`repoRoot`) | `workspaceSlug` + `repoRoot` + `readOnlyRoots` captured; gate **G0-intake** created; no cross-loading of entry files |

The maintainer-only `FRAMEWORK_SMOKE` is the safe default when you do not have access to a consumer workspace. See [`docs/ONBOARDING.md`](ONBOARDING.md) § Maintainer-only.
Run `./scripts/framework_smoke.sh` to exercise its disposable CLI walkthrough;
the script reports the workspace and log paths for a live Cursor or Claude
review, but does not replace that human sign-off.

## Framework tiers

| Tier | Command | Gurobi needed? | Purpose |
|------|---------|----------------|---------|
| **smoke** | `./scripts/run_tests.sh smoke` | No | Fast: config, hooks schema, dummy hook scripts, evidence CSV validators |
| **unit** | `./scripts/run_tests.sh unit` | No | All tests under `tests/` (includes smoke-marked tests) |
| **integration** | `./scripts/run_tests.sh integration` | No in framework | Runs `tests/integration/`; consumer MIP/evidence integration remains separate |
| **all** | `./scripts/run_tests.sh all` | No in framework | smoke + full unit suite |

## Smoke composition (framework)

Framework smoke is **pytest marker selection**:

```bash
./scripts/run_tests.sh smoke    # runs: pytest tests/ -m smoke -q
```

The smoke suite is every `@pytest.mark.smoke` test under `tests/`, including
configuration/path safety, scaffold preservation, truthful pipeline and runner
gates, bounded scanning, evidence validation, Node parity, distribution
artifacts, mirror generation, documentation links, and the deterministic TeX
fixture. The integration directory is run separately by the `integration` tier.

Note: `./scripts/run_tests.sh unit` runs the full test suite under `tests/` (includes all smoke tests).

## Test fixtures

Framework repo fixtures live under `tests/fixtures/`.

- `tests/fixtures/minimal_workspace/`: a **post-scaffold snapshot** generated from the same code path as the product (`fttp.scaffold.scaffold_workspace`). It is intended for tests that need a small, realistic workspace tree without touching any external `readOnlyRoots`.

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

## Green gate for Python changes (framework repo)

Before HANDOFF for any change under `python/fttp/`, `tests/`, `scripts/`, or `docs/TESTING.md`:

```bash
./scripts/run_tests.sh smoke
./scripts/run_tests.sh unit
```

Record **exit codes** in the closure. If either exit code ≠ 0, the work is **TAREA INCOMPLETA**.

The CI workflow records current test counts in JUnit artifacts. Do not copy a historical count into a release note; a green run must also have zero skips, xfails, failures, errors, and empty selections.

## fttp CLI (after `pip install -e .`)

```bash
pip install -e .
FTTP_CONFIG=examples/paperepn-external.config.json python -m fttp doctor
python -m fttp tables    # runs hooks.tables under repoRoot when configured
./scripts/run_tests.sh smoke
```

Config: copy `templates/workspace.config.example.json` → `fttp.config.json` at **your** repo root, or set `FTTP_CONFIG` to an absolute path.
