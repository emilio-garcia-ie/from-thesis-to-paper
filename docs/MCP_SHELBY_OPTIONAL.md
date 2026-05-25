# ShelbyMCP (optional — Cursor + Claude Code)

The **from-thesis-to-paper (fttp)** pipeline does **not** require ShelbyMCP. You can run archaeology, table export, LaTeX, and smoke tests with filesystem `memory/` only.

Use Shelby when you want **cross-session graph memory** (decisions, discrepancies, LOCKED instance ids, narrative choices) that complements — but does not replace — git-tracked `memory/*.md`.

**Package:** [Studio-Moser/Shelby-MCP](https://github.com/Studio-Moser/Shelby-MCP) (`npm` → `shelbymcp`). Local SQLite; no Docker.

---

## Shelby vs `memory/` (both stacks)

| Layer | Role | Authority |
|-------|------|-----------|
| `memory/*.md` | Catalog, brief, reproducibility, signed tables | **Numeric and policy truth** — commit to git |
| ShelbyMCP | Session graph: decisions, tasks, links between thoughts | **Convenience** — search before re-deriving context; never override catalog |

**Rules for agents (both Cursor and Claude):**

- Do **not** store objective values, gaps, or runtimes in Shelby without pointing to `memory/thesis_experiment_catalog.md` or an approved export.
- On `DISCREPANCY` or `LOCKED <id>`, prefer updating `memory/` first; optional `capture_thought` with `project: paperepn` (or your workspace id).
- Do **not** paste secrets (`.env`, Overleaf passwords) into thoughts.

---

## One-time setup (recommended)

From any directory with Node/npm:

```bash
# Cursor — registers ~/.cursor/mcp.json + Memory Protocol in User Rules
npx shelbymcp setup cursor --forage

# Claude Code CLI — user-scope MCP + ~/.claude/CLAUDE.md protocol + forage skill
npx shelbymcp setup claude-code --forage
```

Drop `--forage` if you only want the MCP tools without scheduled enrichment.

**Restart** Cursor (reload window) and start a **new** Claude Code session after setup.

Upstream detail: [Shelby AGENT-SETUP.md](https://github.com/Studio-Moser/Shelby-MCP/blob/main/docs/AGENT-SETUP.md).

---

## Registration patterns

### Cursor

| Scope | File | When |
|-------|------|------|
| **User (global)** | `~/.cursor/mcp.json` | Default after `setup cursor`; all projects |
| **Project** | `<workspace>/.cursor/mcp.json` | Team template or PaperEPN + Overleaf in one file |

Minimal stdio entry (manual):

```json
{
  "mcpServers": {
    "shelbymcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["shelbymcp"]
    }
  }
}
```

**Memory Protocol:** Cursor **Settings → Rules → User Rules** (or project rules). Without it, tools exist but agents rarely save/search proactively.

Verify: **Settings → MCP** → server `shelbymcp` connected; in chat, tools like `capture_thought`, `search_thoughts`, `explore_graph` appear.

### Claude Code

| Scope | Mechanism |
|-------|-----------|
| **User MCP** | `claude mcp add -s user -t stdio shelbymcp -- npx shelbymcp` (done by `setup claude-code`) |
| **Permissions** | `.claude/settings.local.json` in the workspace — allow `mcp__shelbymcp__*` and `Bash(npx shelbymcp *)` |

Example workspace permissions (gitignore `settings.local.json` if it contains machine-specific paths):

```json
{
  "permissions": {
    "allow": [
      "Bash(npx shelbymcp *)",
      "mcp__shelbymcp__capture_thought",
      "mcp__shelbymcp__search_thoughts",
      "mcp__shelbymcp__get_thought",
      "mcp__shelbymcp__list_thoughts",
      "mcp__shelbymcp__explore_graph",
      "mcp__shelbymcp__manage_edges",
      "mcp__shelbymcp__thought_stats"
    ]
  }
}
```

Claude does **not** use `.cursor/mcp.json` for Shelby.

---

## PaperEPN workspace example

In `mi-investigacion-opt`, a typical layout:

- **Overleaf** — project `.cursor/mcp.json` → `scripts/overleaf_mcp.sh` (see [`OVERLEAF_MCP_SETUP.md`](OVERLEAF_MCP_SETUP.md) in PaperEPN or [`MCP_OVERLEAF_OPTIONAL.md`](MCP_OVERLEAF_OPTIONAL.md)).
- **Shelby** — user-global `~/.cursor/mcp.json` **or** merge `shelbymcp` into the same project `mcp.json` if you prefer one file per repo.

Both agents on the same machine share the **same SQLite graph** when both use user-scope Shelby registration.

---

## What is optional vs required

| Artifact | Required for fttp? |
|----------|-------------------|
| ShelbyMCP server | **No** |
| Memory Protocol (Cursor User Rules / Claude `CLAUDE.md`) | **No**, but strongly recommended if Shelby is enabled |
| `.claude/settings.local.json` allow list | Only for Claude Code in that workspace |
| `memory/agent_stack.md` | Documents stack; cites this file |

**Forbidden:** Treating Shelby search results as numeric authority over catalog + signed `paper_strategy_brief.md`.

---

## Related docs

| Doc | Purpose |
|-----|---------|
| [`docs/sync_cursor_claude.md`](sync_cursor_claude.md) | Parity checklist — Shelby on both stacks |
| [`docs/MCP_OVERLEAF_OPTIONAL.md`](MCP_OVERLEAF_OPTIONAL.md) | Overleaf (separate optional MCP) |
| [`AGENTS.md`](../AGENTS.md) / [`CLAUDE.md`](../CLAUDE.md) | Entry pointers |
| `memory/agent_stack.md` (user workspace) | Token budget + component table |

## Quick decision

- **No Shelby:** Valid. Use `memory/` + session handoffs (`HANDOFF:` in subagent prompts).
- **Cursor only:** `npx shelbymcp setup cursor --forage` + verify MCP connected.
- **Claude only:** `npx shelbymcp setup claude-code --forage` + workspace permissions.
- **Both (recommended for PaperEPN):** Run both setup commands; keep catalog numbers in `memory/`, graph notes in Shelby.
