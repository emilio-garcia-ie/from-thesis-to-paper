# First-use QA — 2026-09-07

This record covers the disposable framework walkthrough. It does not claim
scientific validity, real LaTeX compilation, Gurobi execution, Overleaf access,
or publication.

## CLI walkthrough

The following was run in a fresh temporary workspace with Python 3.11:

| Action | Result |
|---|---|
| `fttp scaffold --slug qa-ws --parent <tmp>` | exit 0; template and executable launcher created |
| `fttp doctor` | exit 0 with explicit placeholder-hook warnings |
| `fttp pipeline` before hook replacement | exit 1 at `tables`; later stages did not run |
| edit `README.md`, then `fttp scaffold --force` | exit 0; edited bytes remained unchanged |
| replace stage hooks and compile fixture | `fttp pipeline` exit 0; non-empty PDF fixture verified |

The temporary workspace contained no thesis files, credentials, network calls,
or external integration configuration. Wheel and sdist walkthroughs used the
same scaffold checks outside the checkout.

A fresh rerun against the final worktree reproduced every row above: scaffold
and doctor exited 0, the unconfigured pipeline exited 1 at `tables`, `--force`
preserved an edited README byte-for-byte, and configured offline hooks produced
all stage markers plus a non-empty PDF with pipeline exit 0.

The 110-test Python suite passed on 3.10, 3.11, and 3.14. Node 22 and Node 18
ran the full wrapper parity tests; Node 18 was supplied through `npx`.

## Stack review scope

The canonical `AGENTS.md`/Cursor rules, `CLAUDE.md`, and generated 18-skill
mirrors were inspected for the same install → scaffold → doctor → hook/pipeline
boundary. Automated checks verify both mirror trees and link rebasing. A live
Cursor or Claude interactive session was not available in this execution
environment, so interactive prompt wording and IDE-specific rendering remain a
manual follow-up before release sign-off. The installed Cursor agent reports
`Not logged in`. An attempted disposable Claude `--print` smoke session exited
with code 1 before starting with `Credit balance is too low`; it made no
workspace changes and ran no framework commands.

## Interactive sign-off checklist

Run `./scripts/framework_smoke.sh` from the framework checkout before the
interactive review. It creates and retains a disposable workspace, checks the
scaffold → doctor → expected incomplete-pipeline → `--force` preservation path,
and prints its workspace and pipeline-log paths. It does not replace the live
Cursor and Claude review below.

- [ ] Cursor `FRAMEWORK_SMOKE`: a fresh session reviewed entry files and
  mirrors, then completed the disposable scaffold → doctor → incomplete
  pipeline flow. **Reviewer/date:** ____________________
- [ ] Claude `FRAMEWORK_SMOKE`: a fresh session repeated the same flow without
  requesting thesis paths, credentials, or external uploads. **Reviewer/date:**
  ____________________
- [ ] Both sessions confirmed that editing a workspace file followed by
  `--force` preserves the edit and recorded the observed exit codes.
  **Reviewer/date:** ____________________
