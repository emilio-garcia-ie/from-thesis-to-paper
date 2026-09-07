# Production readiness record

## Candidate

The production candidate is FTTP 0.2.0 on branch
`codex/fttp-safe-refactor`. The original damaged checkout remains untouched.

## Automated evidence

- `scaffold --force` preflights all managed paths, existing configuration, and
  read-only-root boundaries before copying template files.
- `env-suggest` bounds actual `scandir` iteration, not only its reported count.
- Interrupts return a standard nonzero result without a traceback; Python hooks
  can use `FTTP_HOOK_PYTHON`.
- Wheel/sdist resources carry consumer guides, memory templates, skills, and
  one selected Cursor, Claude, or Codex integration.
- The release ZIP includes an offline private installer, wheel, sdist, license,
  and SHA-256 checksums. Installation never edits shell profiles or workspaces.

## Remaining release gates

The implementation is not yet a published production release. Before release,
fresh users must complete the signed Cursor, Claude Code, and Codex
walkthroughs. Hosted CI passed all declared jobs for implementation commit
[`c374659`](https://github.com/emilio-garcia-ie/from-thesis-to-paper/commit/c374659d2eb63cb1e12e15aac594f5883ea75ded)
in [run 34171496032](https://github.com/emilio-garcia-ie/from-thesis-to-paper/actions/runs/34171496032).
A maintainer must then explicitly approve merging, tagging, and publishing the
GitHub Release.

## Manual QA checklist

For each selected agent: download the candidate ZIP, run `bash install.sh`,
create a workspace with `fttp init`, open only that workspace, and follow
`GETTING_STARTED.md`. Record version, ZIP checksum, elapsed time to first
intake, observed commands, and a before/after workspace manifest. Confirm that
no thesis data, credentials, external upload, or approval action is requested.
