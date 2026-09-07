# Refactor contract

This document is the executable contract for the safe and reproducible FTTP
refactor. It preserves the existing Python and Node command names while making
failure, path, packaging, and generated-workspace behavior explicit.

## Boundaries

- `fttp.config.json` wins over `workspace.config.json`; `FTTP_CONFIG` wins over
  both. The example configuration is documentation only.
- `repoRoot`, `paper.dir`, `paper.mainTex`, venue paths, evidence paths, and
  hooks are resolved and checked before a write or subprocess starts.
- Read-only roots may not overlap `repoRoot` in either direction, including
  after symlink resolution. Hooks are trusted local code and run without a
  shell.
- `--force` fills missing scaffold files. It never replaces an existing file,
  rewrites an existing config, or substitutes placeholders in user content.
- `env-suggest --write` creates a new file and refuses an existing target.

## Failure and output contract

- Exit code `0` means the requested operation completed. Expected configuration,
  I/O, and child-process failures return `1`; argparse usage failures return `2`.
- Generated hook placeholders fail with an actionable setup message. A
  pipeline cannot succeed through a placeholder or through a missing compile
  hook.
- A compile hook is successful only when the active expected PDF exists and is
  non-empty. Standalone PDF checking is labeled as an existence check and does
  not claim freshness.
- Test runners preserve pytest failures and never fall back to doctor or a
  passing stub. Empty or missing required test suites fail.
- The Node wrapper delegates complete argv and Python's exit/output behavior;
  it does not maintain a second configuration implementation.

## Bounded scans and evidence

Environment scanning defaults to 50 notebooks, 200 Python files, 10,000
visited entries, 5 MiB per file, and 50 MiB total input. Traversal is sorted,
prunes `.git`, `.venv`, `node_modules`, and `__pycache__`, and never follows
symlinks. Partial or malformed scans are reported and return non-zero.

Evidence helpers preserve the existing public function names and return shapes.
Gurobi status labels are defined once and CSV validation streams rows while
retaining the materializing `load_lineage_rows` helper.

## Distribution and sources of truth

`templates/paper-workspace/` and `skills/` are canonical. Editable clones use
those paths directly; wheels and source distributions carry a generated copy
of the workspace templates under `fttp/_templates/`. IDE skill mirrors are
generated from `skills/` and checked for deterministic, rebased links.

No consumer evidence is migrated. No publisher template, credential, private
workspace, or external integration is bundled. CI validates artifacts and
tests but does not publish or deploy them.

## Traceability

F01–F15 are mapped to the implementation cards in the approved refactor plan
supplied with this change. Recovery of the damaged checkout is recorded
outside the repository; the original checkout remains untouched and is backed
up beside it.
