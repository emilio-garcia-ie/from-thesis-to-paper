# PaperEPN workspace ↔ fttp framework split

> **Canonical framework repo:** [`from-thesis-to-paper`](../README.md) (sibling folder under `PaperEPN/`)  
> **Consumer workspace:** `mi-investigacion-opt` — paper, memory, experiments, archaeology scripts (not shipped in fttp).

## Two repos

| Repo | Typical path | Contains |
|------|--------------|----------|
| **from-thesis-to-paper** | `Desktop/PaperEPN/from-thesis-to-paper` | `python/fttp`, CLI, skills, templates, examples, orchestration plans |
| **mi-investigacion-opt** | `Desktop/PaperEPN/mi-investigacion-opt` | `paper/`, `memory/`, `codigo/`, `experimentos/`, consumer `scripts/` |

The framework was extracted from an early monorepo layout. **Framework changes belong only in `from-thesis-to-paper`.**

## Using the framework from PaperEPN (manual, post-merge)

```bash
pip install -e /path/to/from-thesis-to-paper

cd /path/to/mi-investigacion-opt
cp /path/to/from-thesis-to-paper/examples/paperepn-external.config.json fttp.config.json
# Edit repoRoot and hooks paths to match your machine

FTTP_CONFIG=fttp.config.json python -m fttp doctor
./scripts/run_tests.sh smoke   # consumer tier (e.g. 18/18 when fully configured)
```

See [`examples/README.md`](../examples/README.md) and [`docs/ONBOARDING.md`](ONBOARDING.md).

## Duplicate copies in the consumer repo

Until removed, `mi-investigacion-opt` may still contain **legacy copies** of `python/fttp/`, `skills/`, or `templates/`. Treat **`from-thesis-to-paper` as source of truth** for framework code; the workspace keeps PaperEPN-specific tests and scripts.

## Cursor multi-root (recommended)

Add both folders to the Cursor workspace:

1. `from-thesis-to-paper` — `REPO_FTTP`
2. `mi-investigacion-opt` — `REPO_WORKSPACE`

Orchestration prompts: set `REPO_FTTP` to the framework path; writable edits for paper/memory go to `REPO_WORKSPACE`.

## Related

- [`examples/paperepn-external.config.json`](../examples/paperepn-external.config.json) — illustrative config with `hooks` and `venueProfiles`
- [`docs/PAPER_PRODUCTION_PIPELINE.md`](PAPER_PRODUCTION_PIPELINE.md) — hooks-first pipeline contract
