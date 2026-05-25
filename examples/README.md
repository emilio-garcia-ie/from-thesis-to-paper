# External case study examples

These files document how to point **from-thesis-to-paper** (`fttp`) at a real thesis workspace. They ship **placeholder paths only** — no verification data, no secrets, and no git submodule.

## PaperEPN is external

[PaperEPN](https://github.com/) (`mi-investigacion-opt` and sibling folders) is a **portfolio case study**, not part of this framework repository:

| What | In this repo? |
|------|----------------|
| Agent orchestration, core skills, OR pack stubs | Yes |
| EVRP thesis tables, catalogs, OneDrive logs (~57 GB) | **No** — stays in the user workspace |

Do not add PaperEPN as a submodule or copy verification trees into `examples/`.

## Config files

| File | Purpose |
|------|---------|
| [`paperepn-external.config.json`](paperepn-external.config.json) | Illustrative multi-root layout matching PaperEPN roles (see `AGENTS.md` in the active repo) |
| [`sample-workspace.config.json`](sample-workspace.config.json) | Minimal generic template for any thesis-to-paper project |

Schema matches [`templates/workspace.config.example.json`](../templates/workspace.config.example.json). Required keys: `workspaceName`, `repoRoot`, `paper.dir`, `paper.mainTex`.

## How to use

1. Copy `sample-workspace.config.json` (or adapt `paperepn-external.config.json`) to your **writable** project root as `fttp.config.json` or `workspace.config.json`.
2. Replace every `/path/to/...` placeholder with absolute paths on your machine.
3. Set `readOnlyRoots` to thesis notebooks and verification folders agents must not edit.
4. Optionally set `FTTP_CONFIG` to an absolute path when the config file lives outside the cwd:

   ```bash
   export FTTP_CONFIG=/path/to/your-project/fttp.config.json
   ```

5. Keep Overleaf credentials in `.env` (see `docs/OVERLEAF_MCP_SETUP.md`); never commit `.env` or real `thesis.overleafProjectId` values in public repos.

## PaperEPN folder roles (reference)

When filling `paperepn-external.config.json`, map paths to these roles (from PaperEPN `AGENTS.md`):

| Role | Edit? |
|------|-------|
| `mi-investigacion-opt/` — active repo (`codigo/`, `paper/`, `memory/`, `scripts/`) | **Yes** → `repoRoot` |
| `Thesis Code/` — master notebooks | **Read-only** |
| OneDrive `Models comparison_/` — Ch. 4 verification | **Read-only** |
| OneDrive `multigrafo/` — Ch. 5 verification | **Read-only** |
| OneDrive `inst_generation/` — GIS instances | **Read-only** |
| OneDrive `Pilot1 …/` — spatio-temporal EDA pilot | **Read-only** |

Enable `"packs": ["optimization-or"]` only when the optimization-or skill pack is installed and Gurobi workflows apply.

## Related docs

- [`docs/PORTFOLIO.md`](../docs/PORTFOLIO.md) — framework vs PaperEPN boundary
- [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) — config keys and repository layout
- [`docs/PACKS.md`](../docs/PACKS.md) — optional packs
