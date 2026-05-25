# PaperEPN workspace ↔ fttp framework split

> **Canonical framework repo:** [`/Users/emilio/Desktop/PaperE.`](.)  
> **This repo (`mi-investigacion-opt`):** PaperEPN **user workspace** — paper, memory, experiments, archaeology scripts.

## Two repos (option 2)

| Repo | Path | Contains |
|------|------|----------|
| **from-thesis-to-paper** | `.` | `python/fttp`, CLI, skills, templates, examples, orchestration plans |
| **mi-investigacion-opt** | this directory | `paper/`, `memory/`, `codigo/`, `experimentos/`, PaperEPN `scripts/` |

The framework was initially built inside `mi-investigacion-opt` (B1–B12). It was **extracted** to a sibling folder for open-source publication.

## Using the external framework from this workspace

```bash
# Install Python package from sibling repo
pip install -e .

# Doctor (from workspace root)
cd /Users/emilio/Desktop/PaperEPN/mi-investigacion-opt
FTTP_CONFIG=fttp.config.json node ./packages/cli/src/cli.js doctor
```

Create `fttp.config.json` here via **SA0 CONSUMER_ONBOARD** (see `docs/creacion-de-agentes.md` in the framework repo).

## Duplicate copies in this repo

Until you remove them, `mi-investigacion-opt` may still contain **copies** of framework paths (`python/fttp/`, `packages/`, `skills/`, `templates/`). Treat **`from-thesis-to-paper` as source of truth** for framework changes; this workspace keeps PaperEPN-specific tests and scripts.

## Cursor multi-root (recommended)

Add both folders to the Cursor workspace:

1. `from-thesis-to-paper` — `REPO_FTTP`
2. `mi-investigacion-opt` — `REPO_WORKSPACE`

Prompts: set `REPO_FTTP` to the framework path above.

## Legacy path note

Older docs mention `/Users/emil.` (home directory). The extracted repo lives under **PaperEPN**: `Desktop/PaperE.`.
