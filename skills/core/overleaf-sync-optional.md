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
2. `memory/overleaf_paper_project.md` if present — **paper project only**.
3. `memory/overleaf_thesis_project.md` — **read-only** archaeology; never write.
4. Local `paper/main.tex` is source of truth unless user says otherwise.

## Steps

1. Confirm MCP doctor/login without printing credentials.
2. **Pull** (read) thesis project only when doing table archaeology — separate session from SA12.
3. For **paper** project: diff local vs remote; prefer local git-tracked `paper/` for submission builds.
4. If syncing upward: only `paper/` files user approved; no bulk sync of verification data.
5. Log actions in `memory/overleaf_sync_log.md` with timestamp and direction pull/push.
6. Never store passwords in committed files — use `.env` gitignored.

## Forbidden

- Writing to thesis Overleaf from this skill.
- Adding GurobiMCP or non-documented MCP tools.
- Treating Overleaf as authoritative for numeric table cells over signed catalog/brief.

## Verify

- Sync log entry exists OR explicit “Overleaf skipped — not configured”.
- No modifications under read-only thesis project paths on disk.
- HANDOFF → SA13 when user wants submission package.
