# Reproducibility — `minimal-ws`

> **Tier policy:** Tier A = artifacts inside this Git repo; Tier B = external read-only trees cited by path only.

## Repository access

| Resource | Path (repo-relative) |
|----------|----------------------|
| This guide | `paper/REPRODUCIBILITY.md` |
| Experiment catalog | `memory/thesis_experiment_catalog.md` |
| Evidence bundle | `experimentos/evidence/` (`manifest.json`, `log_lineage.csv` when created) |
| Table fragments | `paper/tables/*.tex` (generated; do not hand-edit numeric cells without re-export) |
| Solver code (optional) | `codigo/` |
| Smoke / integration tests | `tests/` (add when enabling `codigo/` replay) |

**Public URL (fill after release):** TBD — e.g. `https://github.com/your-org/minimal-ws`

## Tier A — in-repo replication

Document locked golden experiments here after SA3–SA4:

| ID | Model | Scenario | Instance | Objective (log) |
|----|-------|----------|----------|-----------------|
| TBD | TBD | TBD | TBD | TBD |

- Registry: `experimentos/fixtures/golden_reference.json` (create when fixtures exist)
- Checks: `./scripts/run_tests.sh smoke` then `integration` when tests are added

## Tier B — external read-only sources

List paths **outside** this repo that reviewers may request access to separately. Do **not** copy multi-GB verification trees wholesale; respect `copyPolicy.maxArtifactMb` in `fttp.config.json`.

| Source role | Absolute path (example) | What was copied into this repo |
|-------------|-------------------------|--------------------------------|
| Thesis notebooks | `/path/to/thesis-notebooks` | TBD — see `memory/intake_report.md` |
| Verification runs | `/path/to/verification-data` | Summaries only → `experimentos/evidence/` |

Record copies in `memory/intake_report.md` and discrepancies in `memory/discrepancy_registry.md`.

## Environment

| Component | Version / note |
|-----------|----------------|
| Python | 3.10+ recommended |
| Gurobi | Optional; required only for exact MIP replay (`optimization-or` pack) |
| LaTeX | `pdflatex`, `bibtex` (venue-specific toolchain after SA1) |
| fttp framework | Clone `from-thesis-to-paper`; set `PYTHONPATH` or use workspace `scripts/run_tests.sh` |

## Evidence honesty

- Use **TBD** when a cell is not anchored to catalog, thesis table, or approved export.
- Use **DISCREPANCY** when log vs catalog vs thesis disagree — document in `memory/discrepancy_registry.md`.
- Prefer Excel/CSV summaries over dumping multi-GB `.log` files into Git or chat.

## Overleaf

- **Thesis project:** read-only archaeology (optional MCP).
- **Paper project:** same display name as `workspaceSlug`; SA12 may sync `paper/` only.
- Credentials: `.env` (gitignored) — see `.env.example`.

## Verification commands

```bash
# From workspace root after SA0 fills fttp.config.json
./scripts/run_tests.sh smoke

# Framework doctor (from fttp clone, with FTTP_CONFIG set)
export FTTP_CONFIG="$(pwd)/fttp.config.json"
python -m fttp doctor
```
