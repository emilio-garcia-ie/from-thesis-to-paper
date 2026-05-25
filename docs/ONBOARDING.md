# End-user onboarding (install → configure → verify)

The framework does **not** collect thesis or paper paths during BUILD (B1–B12). The **installer** collects them in SA0 **CONSUMER_ONBOARD**.

## Steps

1. **Install** — clone this repo or `pip install -e /path/to/from-thesis-to-paper`; optional `npm install` in `packages/cli/`.
2. **Create workspace** — a separate writable directory for your thesis + paper (e.g. PaperEPN `mi-investigacion-opt` with `memory/`, `paper/`, `experimentos/`).
3. **Onboard** — run Cursor prompt **SA0 `MODO: CONSUMER_ONBOARD`** (see [`creacion-de-agentes.md`](creacion-de-agentes.md)) or future `fttp init`. You will answer **nine** questions:
   - **A.** Writable `repoRoot`; journal `paper.dir` and `paper.mainTex` (default `paper/` + `main.tex`)
   - **B.** Thesis source: `local` | `overleaf` | `both`; local thesis path; Overleaf **thesis** project id ([`OVERLEAF_PROJECT_ID.md`](OVERLEAF_PROJECT_ID.md)); Overleaf MCP credentials in `.env` only ([`MCP_OVERLEAF_OPTIONAL.md`](MCP_OVERLEAF_OPTIONAL.md); workspace may add [`OVERLEAF_MCP_SETUP.md`](OVERLEAF_MCP_SETUP.md))
   - **C.** Optional verification READ-ONLY roots; domain pack (`optimization-or` or none); agent chat language (`es` / `en`)
4. **Verify** — `npx from-thesis-to-paper doctor` in the workspace (exit 0).
5. **RUN** — SA1 → SA13 in the workspace repo.

## Config written by SA0

`fttp.config.json` from [`templates/workspace.config.example.json`](../templates/workspace.config.example.json) — includes `paper.*`, `thesis.source`, `thesis.overleafProjectId`, `readOnlyRoots[]`, `packs[]`.

`memory/intake_report.md` from [`templates/memory/intake_report_TEMPLATE.md`](../templates/memory/intake_report_TEMPLATE.md) — no TBD on paper/thesis paths after CONSUMER onboarding.

## Maintainer smoke (post-B12)

Use SA0 `MODO: FRAMEWORK_SMOKE` in this repo only — placeholders, **no** nine consumer questions, no real user thesis data.

## Example workspace

See [`WORKSPACE_EXAMPLE_PAPEREPN.md`](WORKSPACE_EXAMPLE_PAPEREPN.md).
