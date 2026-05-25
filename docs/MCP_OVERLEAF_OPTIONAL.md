# Overleaf MCP (optional)

The **from-thesis-to-paper (fttp)** core pipeline does **not** require Overleaf or any MCP server. You can run evidence archaeology, table export, LaTeX builds, and smoke tests entirely from local `paper/`, `memory/`, and read-only verification trees.

Use Overleaf MCP only when you want agents to **read** thesis LaTeX on Overleaf (table labels, narrative archaeology) or optionally sync a **separate** paper Overleaf project.

## Two Overleaf projects (do not conflate)

| Project | Role for agents | Canonical source |
|---------|-----------------|------------------|
| **Thesis** | **Read-only** — compare thesis tables with `memory/thesis_experiment_catalog.md` and `paper/tables/` | Overleaf thesis + local cache; **never** treat Overleaf as the numeric authority over signed catalog/brief |
| **Paper (submission)** | Optional sync target (SA12) | **Local `paper/main.tex`** and git-tracked `paper/` — submission manuscript is edited and built here |

Discovery and paths for the thesis project live in [`memory/overleaf_thesis_project.md`](../memory/overleaf_thesis_project.md). A paper-only project id (if you use one) belongs in `memory/overleaf_paper_project.md` (create when needed); it is separate from the thesis id.

## What is optional vs already in the repo

| Artifact | Required for fttp? | Notes |
|----------|-------------------|--------|
| Overleaf MCP server | **No** | Convenience for thesis table archaeology |
| `.cursor/mcp.json` | **No** | This repo may ship an example registration; you can omit or disable it |
| `scripts/overleaf_mcp.sh` | Only if you enable MCP | Loads gitignored `.env` and starts `overleaf-mcp` |
| [`docs/OVERLEAF_MCP_SETUP.md`](OVERLEAF_MCP_SETUP.md) | If you enable MCP | Step-by-step install, login, and tool list |

**Not in scope:** Prism or any Prism–Overleaf integration. Do not add, document, or require Prism for PaperEPN / fttp.

## MCP registration pattern (describe, do not commit secrets)

When enabled, Cursor reads `.cursor/mcp.json` at the workspace root. A typical pattern (paths may differ on your machine):

```json
{
  "mcpServers": {
    "overleaf": {
      "command": "<repo>/scripts/overleaf_mcp.sh",
      "env": {
        "LATEX_OUTPUT_DIR": "<cache-dir>",
        "PDF_DOWNLOAD_DIR": "<repo>/paper/overleaf_downloads"
      }
    }
  }
}
```

The launcher script sources **`.env`** (gitignored). Placeholders and variable names are in [`.env.example`](../.env.example) — copy to `.env` locally; **never** commit real passwords or session tokens.

Optional env vars (see setup doc):

- `OVERLEAF_EMAIL`, `OVERLEAF_PASSWORD` — login (free tier OK)
- `OVERLEAF_THESIS_PROJECT_ID` — thesis project hex id after `overleaf_list_projects`
- `OVERLEAF_MCP_BIN` — override binary path if needed

## Agent rules (thesis vs paper)

**Thesis Overleaf**

- Default: **read-only** (`overleaf_read_file`, `overleaf_list_files`, optional compile/PDF for checks).
- Do not edit thesis sources from agents unless the user explicitly requests it.
- Prefer cached files under `~/.overleaf-mcp/` or MCP metadata for large `.tex` files (token protection).

**Paper manuscript**

- Write and verify in local `paper/` (IMRaD, `paper/tables/*.tex`, `./scripts/run_tests.sh smoke`).
- SA12 ([`overleaf-sync-optional`](../.cursor/skills/overleaf-sync-optional/SKILL.md)): optional pull/push for a **paper** project only, with user approval; log in `memory/overleaf_sync_log.md`.

Numeric cells in the submission paper must follow the signed strategy brief and catalog — not unverified Overleaf copies.

## Security

- **Never** commit `.env`, Overleaf passwords, `olp_` Git tokens, or browser session exports.
- Keep `.env` in `.gitignore`; use `.env.example` for variable **names** only.
- Do not paste credentials into chat, `memory/`, or committed JSON.
- `paper/overleaf_downloads/` is for local PDF snapshots — gitignored if large or sensitive.

## Related docs

| Doc | Purpose |
|-----|---------|
| [`docs/MCP_SHELBY_OPTIONAL.md`](MCP_SHELBY_OPTIONAL.md) | Optional graph memory (Cursor + Claude) |
| [`docs/OVERLEAF_MCP_SETUP.md`](OVERLEAF_MCP_SETUP.md) | Install Playwright, first login, MCP tools, verify |
| [`memory/overleaf_thesis_project.md`](../memory/overleaf_thesis_project.md) | Thesis project id, chapter paths, table labels |
| [`AGENTS.md`](../AGENTS.md) | Workspace Overleaf policy (read-only thesis) |
| [`docs/EXECUTOR_GUIDE.md`](EXECUTOR_GUIDE.md) | Subagent closure and handoff tokens |

## Quick decision

- **No Overleaf / no MCP:** Valid. Use thesis PDF, local exports, Excel summaries, and `memory/thesis_experiment_catalog.md`.
- **Thesis archaeology only:** Enable MCP, set thesis project id, read-only tools — follow `OVERLEAF_MCP_SETUP.md`.
- **Optional paper sync:** Separate Overleaf project + SA12; local `paper/` remains canonical unless you state otherwise.
