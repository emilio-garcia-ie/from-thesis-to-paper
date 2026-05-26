# User approval log (template — SA0 init)

> **Copy to:** `memory/user_approval_log.md` during SA0 — start with header rows only; add one row per gate after user `APPROVED:` / `APROBADO:` reply.  
> **Gate definitions:** [docs/USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md) — agents must not HANDOFF to the next SA until the relevant row is `approved` or `approved_with_edits`.  
> **Protocol:** `AUDIT:` → `APPROVE_ASK:` → user token → append row below.

**Secrets:** Do not paste passwords, tokens, or full `.env` contents in **notes**.

---

## How to use

1. Agent issues `AUDIT: <gate_id>` with artifact paths and a short checklist.
2. User replies `APPROVED: <gate_id>` (EN) or `APROBADO: <gate_id>` (ES), or requests edits.
3. Agent appends a row with `user_status`, `approved_at` (ISO 8601), and `notes`.
4. If rejected or pending, agent closes with `TAREA INCOMPLETA` and `BLOQUEADO: no lanzar SA<n+1>`.

Mandatory gates depend on `workflowProfile` in `fttp.config.json` — see [USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md) § Mandatory gates by `workflowProfile`.

---

## Approval rows

| gate_id | SA | artifact_paths | user_status | approved_at | notes |
|---------|-----|----------------|-------------|-------------|-------|
| `G0-intake` | SA0 | `fttp.config.json`, `memory/intake_report.md`, `.env.example` | `TBD` | `TBD` | `TBD` — RO paths; slug = folder + Overleaf paper name; workflowProfile; writingMode; venue stub |
| `G1-venue` | SA1 | `memory/venue_policy.md`, `paper/JOURNAL_GUIDELINES.md`, `paper/latex/**`, `memory/venue_template_manifest.md` | `TBD` | `TBD` | `TBD` |
| `G2-narrative` | SA2 | `memory/narrative_interview.md` | `TBD` | `TBD` | `TBD` |
| `G2b-glossary` | SA2b | `memory/glossary_thesis_en.md` | `TBD` | `TBD` | `TBD` |
| `G4-evidence` | SA4 | `memory/thesis_experiment_catalog.md`, `memory/discrepancy_registry.md`, `experimentos/evidence/*` | `TBD` | `TBD` | `TBD` — skip row if `paper_only` |
| `G7-strategy` | SA7 | `memory/paper_strategy_brief.md` | `TBD` | `TBD` | `TBD` |
| `G8-prose` | SA8 | `paper/main.tex`, `memory/provenance_map.md` | `TBD` | `TBD` | `TBD` — if `thesis_adapt` or `hybrid` |
| `G9-figures` | SA9 | `paper/tables/*.tex`, `paper/figures/*` | `TBD` | `TBD` | `TBD` |
| `G6-repro` | SA6 | `paper/REPRODUCIBILITY.md`, README | `TBD` | `TBD` | `TBD` — if `paper_audit_repro` or `full_pipeline` |
| `G12-overleaf` | SA12 | `memory/overleaf_sync_log.md` | `TBD` | `TBD` | `TBD` |
| `G13-submit` | SA13 | submission checklist, final PDF | `TBD` | `TBD` | `TBD` |

**Optional rows** (add when SA runs): SA5 refactor, SA10 review, SA11 port — include `artifact_paths` and same columns.

### Column reference

| Column | Description |
|--------|-------------|
| `gate_id` | e.g. `G0-intake` — must match [USER_APPROVAL_GATES.md](../../docs/USER_APPROVAL_GATES.md) |
| `SA` | Agent id that produced the artifact |
| `artifact_paths` | Comma-separated relative paths from repoRoot |
| `user_status` | `approved` \| `approved_with_edits` \| `rejected` \| `pending` |
| `approved_at` | ISO-8601 timestamp when user approved |
| `notes` | User corrections summary; no secrets |

---

## Profile reminder (fill at SA0)

| Field | Value |
|-------|--------|
| **workflowProfile** | `TBD` |
| **mandatory_gate_ids** | `TBD` — comma-separated list shown to user |
