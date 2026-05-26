---
name: overleaf-sync-optional
description: SA12 optional Overleaf sync for paper project only — read-only thesis project
---

# Overleaf sync optional (SA12)

## Triggers

- Async after SA9 (`SA12 ~> after SA9` in launch map).
- User configures Overleaf MCP and **paper** (not thesis) project id.
- Optional; core pipeline works without Overleaf.

## Read order

1. `docs/MCP_OVERLEAF_OPTIONAL.md` (or `docs/OVERLEAF_MCP_SETUP.md` in PaperEPN staging).
2. `fttp.config.json` → `workspaceSlug`, `overleafPaper` — display name **must match slug** ([docs/WORKSPACE_MODEL.md](../../docs/WORKSPACE_MODEL.md) §2).
3. `memory/overleaf_paper_project.md` if present — **paper project only** (same slug as workspace).
4. `memory/overleaf_thesis_project.md` — **read-only** archaeology; **never write**.
5. Local `paper/main.tex` is source of truth unless user says otherwise.
6. `memory/user_approval_log.md` — write **G12-overleaf** after sync when performed (below).

## Two Overleaf projects (mandatory)

| Project | Config / memory | Agent access |
|---------|-----------------|--------------|
| **Thesis** | `thesis.overleafProjectId`, `memory/overleaf_thesis_project.md` | **Read-only** archaeology (table/equation lookup) — separate session from SA12 |
| **Paper** | `overleafPaper.projectId`, display name = **`workspaceSlug`** | SA12 may sync **only** `paper/` subtree |

**NEVER write** to the thesis Overleaf project from this skill or any SA12 sync step. Violations → **TAREA INCOMPLETA**.

## Steps

1. Confirm MCP doctor/login without printing credentials.
2. **Pull** (read) thesis project only when doing table archaeology — separate session from SA12.
3. For **paper** project: diff local vs remote; prefer local git-tracked `paper/` for submission builds.
4. If syncing upward: only `paper/` files user approved; no bulk sync of verification data.
5. Log actions in `memory/overleaf_sync_log.md` with timestamp and direction pull/push.
6. Never store passwords in committed files — use `.env` gitignored.
7. If sync was performed (push or pull on **paper** project): run **G12-overleaf** AUDIT / APPROVE (below). If Overleaf skipped → log explicit skip; no G12 row required.

## G12-overleaf — AUDIT / APPROVE (when sync performed)

Per [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md). **Blocks SA13** when user wants submission via Overleaf after sync.

After `memory/overleaf_sync_log.md` and file list diff:

```text
AUDIT: G12-overleaf — review memory/overleaf_sync_log.md and paper/ diff vs remote
Checklist:
- Only paper/ subtree synced (no verification data, no memory/ secrets)
- Thesis Overleaf project untouched (read-only archaeology only)
- Push/pull direction and timestamp recorded; local git remains source of truth unless user chose remote-first
APPROVE_ASK: Confirm Overleaf paper project matches your intent. Reply APPROVED: G12-overleaf (EN) or APROBADO: G12-overleaf (ES) or corrections.
```

On user approval: update row **`G12-overleaf`** in `memory/user_approval_log.md`.

**When sync was performed but not approved:**

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA13 — missing approved row for G12-overleaf
```

If Overleaf not configured or user skips sync: document in sync log — **G12 waived**; HANDOFF → SA13 with local PDF only.

## Forbidden

- Writing to thesis Overleaf from this skill.
- Adding GurobiMCP or non-documented MCP tools.
- Treating Overleaf as authoritative for numeric table cells over signed catalog/brief.

## Verify

- Sync log entry exists OR explicit “Overleaf skipped — not configured”.
- Paper Overleaf display name matches `workspaceSlug` when configured (doctor or config check).
- No modifications under read-only thesis project paths on disk or remote thesis project.
- When sync performed: `memory/user_approval_log.md` has **G12-overleaf** `approved` before HANDOFF → SA13.
- HANDOFF → SA13 when user wants submission package.
