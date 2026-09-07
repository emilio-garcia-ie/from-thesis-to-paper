# Refactor execution record

This record keeps recovery and verification evidence separate from consumer
workspaces. It is intentionally concise; detailed test output remains in the
local execution logs.

## Recovery

- Original checkout: `<original damaged checkout>`
- Working checkout: `<isolated refactor checkout>`
- Baseline commit: `60da0c5dd3817fef4a45c0e03659d8f2f0573f26`
- Private backup: `<private archive outside tracked paths>`
- Backup manifest: `<private manifest outside tracked paths>`
- Recovery date: 2026-09-07

The original Git tree is damaged and was not repaired. Ten local overlays were
copied to the isolated checkout after their SHA-256 hashes were compared.

## Baseline

- Recovered remote suite before refactoring: 55 passed.
- With preserved local mirror tests: 58 passed, 3 mirror failures.
- Python source AST and shell syntax checks: passed.
- Wheel build before refactoring: passed, but runtime templates were absent.

## Refactor verification

- Python smoke selection: 110 passed, 0 skipped.
- Python full suite: 110 passed, 0 skipped.
- Combined `./scripts/run_tests.sh all`: smoke and full selections each passed
  110 tests with zero skips.
- Offline integration selection: 1 passed, 0 skipped.
- CI-equivalent JUnit reports passed `ci/check_junit.py`: 110 full tests and 1
  integration test, with no skips, xfails, failures, errors, or empty suites.
- The wheel, sdist, and npm archive passed `ci/check_artifacts.py`; a
  three-entry SHA-256 manifest was generated for the release archives.
- Skill generator: 18 canonical skills × 2 mirrors; `--check` and second
  generation pass are clean.
- Node syntax and shell syntax: passed.
- Wheel and sdist installed outside the checkout and scaffolded equivalent
  workspaces; npm archive contains launcher, manifest, and license.
- The 70-entry original regular-file inventory and a fresh archive extraction
  both rehashed against the private manifest with zero mismatches; damaged
  original Git status remains unrepaired. A companion private metadata
  inventory also matched file modes and symlink targets for all 70 manifest
  entries. That metadata remains outside tracked paths with the private backup.
- First-use CLI walkthrough and its interactive-session limitation are recorded
  in `docs/REFACTOR_QA_2026-09-07.md`.
- D06 interactive Cursor/Claude sign-off remains open because those sessions
  were unavailable. The installed Cursor agent reports `Not logged in`, and a
  disposable Claude `--print` attempt exited with code 1 before starting with
  `Credit balance is too low`; automated framework smoke and the CLI walkthrough
  are complete, but this record is not a final publication sign-off.
- Python 3.10, 3.11, and 3.14 suites: 110 passed each. Node 22 syntax and
  parity tests pass; the four Node parity tests also pass under Node 18
  obtained through `npx`, along with its syntax/version check.
- The clean Python 3.11 environment reports `pip check` clean; the package
  directory passes `npm ci --ignore-scripts`, npm dry-run packing, and Node
  syntax validation.
- The CI workflow's named `smoke`, `unit`, and `integration` entrypoints pass
  locally; separate source-installed JUnit runs report 110 and 1 tests with
  zero skips, xfails, failures, errors, or empty selections.
- The maintainer-only `scripts/framework_smoke.sh` passes locally and now runs
  in the Python CI job; it is a reproducible input to D06, not a substitute
  for the required live Cursor and Claude sign-offs.
- A clean Python 3.11 virtualenv installed `requirements-dev.lock`, installed
  the package with `--no-deps --no-build-isolation`, and passed the direct CI
  JUnit test and integration commands with `PYTHONPATH` unset.
- That same locked environment built the wheel and sdist, packed the npm
  wrapper, and passed the three-archive manifest checker.
- The CI Node 18/22 matrix now installs the Python package and runs the four
  Node/Python parity tests; both runtimes pass locally.
- Clean Python 3.10 and 3.14 environments also installed the package with
  `PYTHONPATH` unset and passed 110 full tests plus 1 integration test each;
  their JUnit reports passed the strict checker.
- Node 18 also passes the package-local `npm ci --ignore-scripts` and dry-run
  pack checks in addition to the parity suite.
- The four pinned GitHub Action SHAs resolve upstream to Node 24-based
  checkout v6.0.3, setup-python v6.3.0, setup-node v6.5.0, and
  upload-artifact v6.0.0.
- Hosted CI [run 34165335701](https://github.com/emilio-garcia-ie/from-thesis-to-paper/actions/runs/34165335701)
  passed all eight jobs at `ac4d462`: Node 18/22 and Python 3.10/3.11/3.14
  on Ubuntu and macOS. It exercised the full test, JUnit, smoke, packaging,
  archive, and Node-parity gates using the Node 24-based action pins.
- A fresh disposable first-use walkthrough passed scaffold, doctor, truthful
  placeholder failure, `--force` byte preservation, and configured offline
  pipeline/PDF checks; details are in the QA record.

## Scope guard

No thesis data, credentials, external service, Gurobi run, publication, or
consumer workspace was modified during recovery.

## Production-readiness follow-up

- The former automated completion claim is corrected by
  [`PRODUCTION_READINESS.md`](PRODUCTION_READINESS.md): the 110-test result
  and hosted run remain historical evidence, but they did not cover the
  subsequently reproduced scaffold escape, scanner-enumeration, installed
  workflow, installer, or live-agent guarantees.
- Candidate `0.2.0` adds transactional scaffold preflight, measured scanner
  traversal limits, cancellation handling, a selected-agent consumer
  workspace, clean console-script artifact tests, and an offline release ZIP.
- Local candidate verification: 130 tests passed with no skips; the consumer,
  distribution, installer, and release-bundle selection passed in clean
  temporary environments. Hosted CI run 34171496032 passed all declared
  platform/Python and Node jobs for `c374659`; fresh Cursor, Claude Code, and
  Codex walkthroughs remain required release gates.

## Task ledger

| Task | Status | Proof / affected scope |
|---|---|---|
| R01 | complete | Private archive and manifest verified against the damaged original; original hashes unchanged. |
| R02 | complete | Isolated checkout at the pinned commit, ten overlays accounted for, `git fsck` passed, baseline recorded. |
| R03 | complete | [`REFACTOR_CONTRACT.md`](REFACTOR_CONTRACT.md) records the locked runtime, path, failure, scanner, evidence, packaging, and mirror rules. |
| G01 | complete | Recovery inventory, contract, and baseline evidence rechecked. |
| S01–S10 | complete | Boundary, scaffold, pipeline, scanner, test-runner, LaTeX-fixture, and offline integration regressions are in `tests/`; the runtime selection passes. |
| G02 | complete | `./scripts/run_tests.sh all`: 110 smoke and 110 full tests, zero skips. |
| C01–C04 | complete | Node parity/transport tests and status/CSV validator tests pass; Python remains the business-logic source. |
| C05–C08 | complete | Wheel/sdist outside-checkout scaffolding, npm archive, and fake-npx launcher tests pass. |
| G03 | complete | CLI, evidence, distribution, launcher, and safety selections pass together. |
| D01–D04 | complete | Canonical content, generated mirrors, links, command references, onboarding, and documentation checks pass. |
| D05 | complete | Locked dev/build metadata, npm lockfile, pinned-action CI workflow, named smoke/unit/integration entrypoints, Node 18/22 parity jobs, JUnit/artifact gates, and three-archive manifest checks are present. Hosted run 34165335701 passed all eight Linux/macOS Python and Node jobs. |
| D06 | pending manual sign-off | Disposable CLI walkthrough is complete; live Cursor and Claude sessions were unavailable and are explicitly recorded as a release follow-up. |
| G04 | pending D06 | Automated verification is green, but final review readiness/publication sign-off requires the interactive evidence in D06. |
| P01 / S01–S05 | complete locally | The production acceptance record, external-write preflight, bounded `scandir` traversal, configuration validation, cancellation handling, and `FTTP_HOOK_PYTHON` tests are present; candidate tests pass locally. |
| U01–U05 / G02 | complete locally | The wheel/sdist bundle local guides, memory, one selected agent layout, and `init`/`start`/`status`; clean installed console-script acceptance tests pass. |
| I01–I02 / G03 | complete locally | The offline private installer and ZIP build/install/rollback/uninstall tests pass with disposable prefixes. |
| D01 | complete locally | Primary documentation now follows download, install, init, and start; support, security, and release guidance are included. |
| D02 | complete for `c374659` | Hosted CI run 34171496032 passed all declared Linux/macOS Python and Node jobs. |
| Q01–Q03 / G04 / R01 | pending | Fresh agent-host walkthroughs, final readiness audit, and the explicitly approved release action remain open. |
