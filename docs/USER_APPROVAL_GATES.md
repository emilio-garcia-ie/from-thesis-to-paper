# User approval gates — audit and approve

> **Audience:** users and agents (SA0–SA13).  
> **Language:** English (closure tokens may appear in Spanish per [EXECUTOR_GUIDE.md](EXECUTOR_GUIDE.md)).

Agents propose artifacts; **you** validate them before the pipeline advances. This complements [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md) (WHY-before-ASK).

---

## Protocol

After producing or updating a gate artifact:

1. **`AUDIT:`** — what to review, file paths, 3–7 bullet checklist.
2. **`APPROVE_ASK:`** — request explicit approval or edits.
3. **No HANDOFF** to the next SA until `memory/user_approval_log.md` has `status: approved` or `approved_with_edits` for that `gate_id`.
4. If you correct content, the agent updates files and issues a **new** `AUDIT` for changed items only.

### User closure tokens (chat)

| Language | Accepted reply |
|----------|----------------|
| English | `APPROVED: <gate_id>` or `OK: <gate_id>` |
| Spanish | `APROBADO: <gate_id>` |

The agent copies ISO-8601 timestamp into the log.

### Agent closure without approval

```text
TAREA INCOMPLETA
BLOQUEADO: no lanzar SA<n+1> — missing approved row for <gate_id>
```

---

## Gate table (G0–G13)

| gate_id | SA | Artifact(s) to review | User checks | Blocks if not approved |
|---------|-----|------------------------|-------------|-------------------------|
| **G0-intake** | SA0 | `fttp.config.json`, `memory/intake_report.md`, `.env.example` (no secrets in log) | RO paths correct; slug = folder + Overleaf paper name; `workflowProfile`, `writingMode`, venue stub; no thesis paths inside paper repo | SA1 |
| **G1-venue** | SA1 | `memory/venue_policy.md`, `paper/JOURNAL_GUIDELINES.md`, `paper/latex/**`, `memory/venue_template_manifest.md` | Page/reference limits plausible; `\documentclass` matches installed files; template license OK to copy | SA7, SA8 |
| **G2-narrative** | SA2 | `memory/narrative_interview.md` | One-sentence contribution; `forbidden_claims`; narrative arc | SA2b, SA7 |
| **G2b-glossary** | SA2b | `memory/glossary_thesis_en.md` | Model names and EN terms correct; add missing jargon | SA8 |
| **G4-evidence** | SA4 | `memory/thesis_experiment_catalog.md`, `memory/discrepancy_registry.md`, `experimentos/evidence/*` | TBD/DISCREPANCY visible; numeric authority (catalog vs log) agreed | SA7, SA8 |
| **G7-strategy** | SA7 | `memory/paper_strategy_brief.md` (signed) | `evidence_path`, allowed tables, `writing_mode`, claims align with G2 and G4 | SA8 |
| **G8-prose** | SA8 | `paper/main.tex` (section or summary diff), `memory/provenance_map.md` if `thesis_adapt` | Voice preserved; no forbidden claims; traceable paragraphs; English IMRaD | SA9 |
| **G9-figures** | SA9 | `paper/tables/*.tex`, `paper/figures/*`, PDF if built | Labels match brief; numbers match evidence; figure resolution vs venue | SA12, SA13 |
| **G6-repro** | SA6 | `paper/REPRODUCIBILITY.md`, paper repo README | In-repo vs external data; smoke commands documented | Public release |
| **G12-overleaf** | SA12 | `memory/overleaf_sync_log.md`, file list diff | Only `paper/` synced; thesis RO untouched; push/pull direction agreed | SA13 |
| **G13-submit** | SA13 | Submission checklist, final PDF | Anonymization, page limit, data/code policy | Portal upload |

**Optional / profile-dependent:** SA5 refactor, SA10 review, SA11 port — add rows to the log when those SAs run; `full_pipeline` may require extra sign-off on `codigo/` changes.

---

## Mandatory gates by `workflowProfile`

Set in SA0 Block C. Fewer profiles mean fewer mandatory checkpoints.

| Profile | Mandatory gates |
|---------|-----------------|
| **`paper_only`** | G0, G1, G2, G2b, G7, G8, G9 |
| **`paper_audit`** | Above + **G4** |
| **`paper_audit_repro`** | Above + **G6** |
| **`full_pipeline`** | All applicable gates above + SA5/refactor sign-off when `codigo/` is touched |

SA0 should tell the user **how many checkpoints** to expect for the chosen profile.

```mermaid
flowchart LR
  G0[G0 intake] --> G1[G1 venue]
  G1 --> G2[G2 narrative]
  G2 --> G2b[G2b glossary]
  G2b --> G4[G4 evidence]
  G4 --> G7[G7 strategy]
  G7 --> G8[G8 prose]
  G8 --> G9[G9 figures]
  G9 --> G12[G12 overleaf]
  G12 --> G13[G13 submit]
```

*`paper_only` skips G4 and G6; `paper_audit` includes G4; `paper_audit_repro` adds G6.*

---

## Log file

Template: `templates/memory/user_approval_log_TEMPLATE.md` (created empty during SA0).

| Column | Description |
|--------|-------------|
| `gate_id` | e.g. `G0-intake` |
| `SA` | Agent id |
| `artifact_paths` | Comma-separated paths |
| `user_status` | `approved`, `approved_with_edits`, `rejected` |
| `approved_at` | ISO-8601 |
| `notes` | User corrections summary |

---

## WHY when asking for approval

Suggested agent wording:

> You are the final authority: I propose and extract, but you confirm this reflects your thesis and meets the journal before we write more.

Canonical rationale per SA0 block: [ONBOARDING_RATIONALE.md](ONBOARDING_RATIONALE.md).

---

## Related docs

| Doc | Contents |
|-----|----------|
| [ONBOARDING.md](ONBOARDING.md) | Install and first RUN |
| [EXECUTOR_GUIDE.md](EXECUTOR_GUIDE.md) | AUDIT/APPROVE_ASK and Mini-Guía |
| [WORKSPACE_MODEL.md](WORKSPACE_MODEL.md) | Writable vs read-only |
