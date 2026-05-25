# Overleaf MCP — Cursor setup (PaperEPN)

Connect Cursor agents to your **thesis LaTeX on Overleaf** (Cap. 4/5 tables, figures, values).

## What is configured

| File | Role |
|------|------|
| `.cursor/mcp.json` | Registers MCP server `overleaf` |
| `scripts/overleaf_mcp.sh` | Loads `.env` and starts `overleaf-mcp` |
| `.env` | Your credentials (**gitignored**) |
| `memory/overleaf_thesis_project.md` | Thesis project id + table file paths (after discovery) |

**Server package:** [sahithreddy/overleaf-mcp](https://github.com/sahithreddy/overleaf-mcp) (`npm install -g overleaf-mcp`).  
Uses browser automation (Playwright) — **works on Overleaf free tier**; no Git token required for read.

## One-time setup (you)

### 1. Credentials

Edit **`.env`** only (gitignored). **Never** put real passwords in `.env.example`.

```bash
cd /Users/emilio/Desktop/PaperEPN/mi-investigacion-opt
cp .env.example .env   # first time only
# Edit .env — NO spaces around = :
#   OVERLEAF_EMAIL=you@example.com
#   OVERLEAF_PASSWORD=yourpassword
```

**Project id:** see [`docs/OVERLEAF_PROJECT_ID.md`](OVERLEAF_PROJECT_ID.md) — copy the 24-character hex from the Overleaf project URL into `fttp.config.json` → `thesis.overleafProjectId` and/or `.env` → `OVERLEAF_THESIS_PROJECT_ID`.

### 2. Playwright (if not already installed)

```bash
npx playwright install chromium
```

### 3. Make launcher executable

```bash
chmod +x scripts/overleaf_mcp.sh
```

### 4. Restart Cursor

**Cursor Settings → MCP** (or reload window). You should see server **`overleaf`** connected.

If it fails, check the MCP log: missing `.env` or wrong password.

### 5. First login (once per machine)

In a Cursor Agent chat:

```
Use the overleaf MCP: call overleaf_login, then overleaf_list_projects.
Find the thesis project (Spanish title / EVRP / EPN). Save the project id in memory/overleaf_thesis_project.md.
```

A Chrome window opens; solve CAPTCHA if prompted. Session persists under `~/.overleaf-mcp/browser-data/`.

## Agent workflow — read thesis tables

After `OVERLEAF_THESIS_PROJECT_ID` is set in `.env` or `memory/overleaf_thesis_project.md`:

```
1. overleaf_read_file(project_id, path_to_table.tex)  — cache only, low tokens
2. Compare values with memory/thesis_experiment_catalog.md
3. Regenerate paper/tables with export_tables_from_catalog.py --mode thesis-mirror
```

Typical thesis paths to search: `main.tex`, `capitulos/capitulo4.tex`, `tablas/`, `tables/`, `chapter4/`.

Use `overleaf_list_files` on the project to discover exact paths.

## Tools available (npm overleaf-mcp)

| Tool | Use for PaperEPN |
|------|------------------|
| `overleaf_list_projects` | Find thesis project id |
| `overleaf_read_file` | Read table `.tex` / `main.tex` |
| `overleaf_list_files` | Discover table file names |
| `overleaf_compile` | Optional PDF check |
| `overleaf_download_pdf` | Optional thesis PDF snapshot |

**Do not** use Overleaf MCP to edit the thesis project from agents unless you explicitly want that — prefer **read-only** for archaeology.

## Alternative: Git-based MCP (paid Overleaf)

If you have **Git integration** on Overleaf, you can switch to Python [`rangehow/overleaf-mcp`](https://github.com/rangehow/overleaf-mcp):

```bash
pip install overleaf-mcp[compile]
```

Env: `OVERLEAF_SESSION` (cookie) + `OVERLEAF_GIT_TOKEN` (`olp_...`).  
Update `.cursor/mcp.json` to `"command": "overleaf-mcp"` with those env vars.  
Not configured by default in this repo.

## Security

- Never commit `.env` or Overleaf passwords.
- `.gitignore` includes `.env` and `paper/overleaf_downloads/`.
- Agents should read thesis Overleaf **read-only**; paper edits stay in `paper/main.tex` locally.

## Verify

```bash
./scripts/overleaf_mcp.sh &
# Should exit immediately if .env missing; otherwise MCP runs on stdio (Ctrl+C)
```

In Cursor Agent: `call ping` on overleaf MCP → `"status": "ok"`.
