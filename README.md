# from-thesis-to-paper

Agent-orchestrated framework: **thesis → evidence audit → journal paper** (IMRaD), with optional **optimization-or** pack (MIP/Gurobi, routing, GIS).

This repository is the **standalone product**. It does not contain a thesis or paper manuscript.

## Quickstart (framework maintainer)

```bash
cd /path/to/from-thesis-to-paper
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"  # or: pip install -e . && pip install pytest
./scripts/run_tests.sh smoke
node packages/cli/src/cli.js doctor
```

## Quickstart (end user — your thesis project)

1. Create or use a **writable workspace** (e.g. clone PaperEPN `mi-investigacion-opt`).
2. Install fttp: `pip install -e /path/to/from-thesis-to-paper` or `npm link` the CLI package.
3. Run onboarding: **SA0 `CONSUMER_ONBOARD`** (Cursor) or future `fttp init` — supplies paths, read-only roots, packs, Overleaf id.
4. `npx from-thesis-to-paper doctor` in your workspace.

See [`docs/creacion-de-agentes.md`](docs/creacion-de-agentes.md) for BUILD (B1–B12) and RUN (SA0–SA13) prompts.

## Layout

| Path | Role |
|------|------|
| `python/fttp/` | Python package (config, pipeline stubs) |
| `packages/cli/` | npm CLI `fttp` / `from-thesis-to-paper` |
| `skills/core/` | Core agent skills (SA0–SA13) |
| `skills/packs/optimization-or/` | Optional OR pack |
| `templates/` | Memory + workspace config templates |
| `examples/` | External case studies (PaperEPN placeholders) |
| `.cursor/plans/` | Orchestration prompts |

## PaperEPN reference workspace

External example (not a submodule):  
`/Users/emilio/Desktop/PaperEPN/mi-investigacion-opt` — see [`examples/README.md`](examples/README.md).

## License

MIT — see [LICENSE](LICENSE).
