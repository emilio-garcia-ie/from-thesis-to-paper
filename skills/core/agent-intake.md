---
name: agent-intake
description: SA0 workspace onboarding — consumer install vs maintainer smoke; paper paths, thesis source, Overleaf MCP, packs
---

# Agent intake (SA0)

## Modes

| Mode | Who | User questions |
|------|-----|----------------|
| **CONSUMER_ONBOARD** | End user after `npm`/`npx` install | **Required** — nine questions (paper, thesis, Overleaf, MCP, roots, pack, language); same contract as future `fttp init` |
| **FRAMEWORK_SMOKE** | Maintainer post-B12 | **Do not ask** the nine consumer questions — placeholders + `intake_report.md` notes onboarding pending |

## Goal

Configure **thesis → journal paper**: writable `paper/` for the manuscript; read-only thesis ground truth (local disk and/or Overleaf); optional verification roots; domain packs.

## Triggers

- End user installs fttp and needs `fttp.config.json` + `memory/`.
- `fttp doctor` reports missing paths.
- User says “intake”, “onboard”, “configure workspace”, “SA0”.
- Before evidence or LaTeX when `memory/intake_report.md` is absent or stale (CONSUMER only).

## Read order

1. `fttp.config.json` or `workspace.config.json` (writable workspace root).
2. `templates/workspace.config.example.json` — `paper.*`, `thesis.source`, `thesis.overleafProjectId`, `readOnlyRoots[]`, `packs[]`.
3. `docs/ARCHITECTURE.md` §1 layers (read-only vs writable).
4. `docs/OVERLEAF_PROJECT_ID.md` — extract 24-char hex from Overleaf URL.
5. `docs/OVERLEAF_MCP_SETUP.md` or framework `docs/MCP_OVERLEAF_OPTIONAL.md` (Overleaf thesis).
6. `docs/PACKS.md` for niche pack choice.
7. `AGENTS.md` and `docs/EXECUTOR_GUIDE.md` closure protocol.

## Ask user — CONSUMER_ONBOARD (do not skip)

**A. Workspace & paper (writable)**

1. Confirm `REPO_WORKSPACE` absolute path (`repoRoot`).
2. **Paper output:** journal manuscript directory (default `paper/`) and main file (default `main.tex`). Create dirs if missing → `fttp.config.json` → `paper.dir`, `paper.mainTex`.

**B. Thesis ground truth (read-only)**

3. **Thesis source:** `local` | `overleaf` | `both`.
4. If **local:** absolute path to thesis notebooks / thesis tree → `readOnlyRoots[]`.
5. If **overleaf** or **both:** Overleaf **thesis** project id — URL `https://www.overleaf.com/project/<24-char-hex>`; copy only the hex; see `docs/OVERLEAF_PROJECT_ID.md`.
6. If **overleaf** or **both:** Overleaf MCP (required for Overleaf thesis):
   - Docs: workspace `docs/OVERLEAF_MCP_SETUP.md` or framework `docs/MCP_OVERLEAF_OPTIONAL.md`.
   - Ask Overleaf **email** + **password** → write **only** to `REPO_WORKSPACE/.env` (gitignored); record `set in .env` in `intake_report.md`; **never** commit or echo password in the report.
   - Install: `overleaf-mcp`, Playwright chromium, `scripts/overleaf_mcp.sh` + `.cursor/mcp.json` if Cursor.
   - First login: `overleaf_login`, `overleaf_list_projects`; create `memory/overleaf_thesis_project.md`.

**C. Experiments & niche**

7. Other READ-ONLY roots — verification, multigraph, inst_generation (optional; no multi-GB copy).
8. Pack `optimization-or` (yes/no) or other packs from `docs/PACKS.md`.
9. Chat language (`es` / `en`).

## Steps — CONSUMER_ONBOARD

1. Copy `REPO_FTTP/templates/memory/*` → `REPO_WORKSPACE/memory/` if missing (do not overwrite user-edited briefs without OK).
2. Ensure `paper/` (or chosen `paper.dir`) exists; add minimal `main.tex` stub **only** if user OK and file missing.
3. Copy `templates/workspace.config.example.json` → `fttp.config.json` — `repoRoot`, `paper.*`, `readOnlyRoots[]`, `packs`, `thesis.source`, `thesis.overleafProjectId`, `thesis.mainTexPath` when relevant.
4. Write `memory/intake_report.md` from `intake_report_TEMPLATE.md` — all answers; **no TBD** on paper/thesis paths.
5. If Overleaf: configure `.env`, verify MCP; copy `docs/OVERLEAF_PROJECT_ID.md` to workspace if missing.
6. `cd REPO_WORKSPACE && npx from-thesis-to-paper doctor` (exit 0).
7. Optional: `./scripts/run_tests.sh smoke` if workspace has tests.

## Steps — FRAMEWORK_SMOKE

1. Copy templates with placeholder paths only (`/path/to/...`).
2. `packs: []` unless testing pack wiring; `thesis.source` may be `local` with placeholders.
3. `intake_report.md` section **Consumer onboarding — pending**; TBD on user answers.
4. `doctor` exit 0; missing `readOnlyRoots` may warn.

## Forbidden

- Copying multi-GB verification folders into the framework repo.
- Editing master notebooks or paths under `readOnlyRoots`.
- Committing `.env` or pasting Overleaf passwords into `intake_report.md` or chat logs in reports.
- Hardcoding one user's OneDrive paths into the published framework repo.
- Inventing experiment counts or table values in intake notes.

## Verify

- `test -f memory/intake_report.md`
- Config JSON valid; `paper.dir` / `paper.mainTex` set.
- **CONSUMER:** `thesis.source` set; Overleaf id + MCP (`.env`) if `overleaf` or `both`.
- **CONSUMER:** HANDOFF → SA1.
- **SMOKE:** no HANDOFF to SA1–SA13.

## Closure

- **SE TERMINÓ LA TAREA COMPLETA (SA0)** — CONSUMER: `paper.dir`/`mainTex` set; `thesis.source` set; `readOnlyRoots` and/or Overleaf id + MCP (`.env`) if applicable; packs and lang recorded; doctor OK.
- **HANDOFF:** CONSUMER → SA1; SMOKE → publish framework only.
- **TAREA INCOMPLETA** — BLOQUEADO: SA1–SA13 (CONSUMER mode only).
